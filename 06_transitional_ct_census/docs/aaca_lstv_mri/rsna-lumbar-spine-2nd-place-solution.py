#!/usr/bin/env python
# coding: utf-8

# * T4 -> P100
# * Replace missing rows insertions at the end
# * Free GPU memory and RAM 

# # Yuji part

# In[ ]:


%%capture
!pip install '/kaggle/input/rsna2024-demo-workflow/natsort-8.4.0-py3-none-any.whl'
!pip install /kaggle/input/notebook0248a0e3f9/pycocotools-2.0.7-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl /kaggle/input/notebook0248a0e3f9/dicomsdl-0.109.3-cp310-cp310-manylinux_2_12_x86_64.manylinux2010_x86_64.whl /kaggle/input/notebook0248a0e3f9/loguru-0.7.2-py3-none-any.whl /kaggle/input/notebook0248a0e3f9/pydicom-2.4.4-py3-none-any.whl /kaggle/input/notebook0248a0e3f9/python_gdcm-3.0.24.1-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl  /kaggle/input/notebook97381653b4/ensemble_boxes-1.0.9-py3-none-any.whl

!pip install -qq /kaggle/working/python-packages/timm-0.9.10-py3-none-any.whl

# # 1, axial level estimation by hengck23's code
# ref: https://www.kaggle.com/code/hengck23/ver-1-demo-workflow-2-stage-approach?scriptVersionId=191553260

# In[ ]:


from glob import glob
debug = False
debug_fold = 2
plot = False
train_test = 'test'

import sys, os
sys.path.append('/kaggle/input/rsna2024-demo-workflow')

from _dir_setting_ import *

import matplotlib
import matplotlib.pyplot as plt

from helper import *
from data import *
from model import *

# STEP0 : SETUP DATA ==========================

cfg=dotdict(
    point_net=dotdict(
        checkpoint='/kaggle/input/rsna2024-demo-workflow/00002484.pth',
        image_size=160,
    ),
)

level_to_label={
    'l1_l2':1,
    'l2_l3':2,
    'l3_l4':3,
    'l4_l5':4,
    'l5_s1':5,
}

#################################################

# study id used for demo
id_df = pd.read_csv(f'{DATA_KAGGLE_DIR}/test_series_descriptions.csv')    

point_net = Net(pretrained=False)
f = torch.load(cfg.point_net.checkpoint, map_location=lambda storage, loc: storage)
state_dict = f['state_dict']
point_net.load_state_dict(state_dict, strict=False)
point_net.cuda()
point_net.eval()
point_net.output_type = ['infer']


from _dir_setting_ import *
from natsort import natsorted
import pandas as pd
pd.set_option('mode.chained_assignment', None) # disable SettingWithCopyWarning

import numpy as np
import pydicom
import glob
import timm
import cv2

from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from pdb import set_trace as st

class dotdict(dict):
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

################################################################################3


# read into volume (np_array) + dicom_header(df)
'''
import notes:
- instance_number may not be sequentially (can have missing num)
- instance_number is 1-indexed

'''

## 3d/2d processing #########################################################
def np_dot(a,b):
    return np.sum(a * b, 1)

def project_to_3d(x,y,z, df):
    d = df.iloc[z]
    H, W = d.H, d.W
    sx, sy, sz = [float(v) for v in d.ImagePositionPatient]
    o0, o1, o2, o3, o4, o5, = [float(v) for v in d.ImageOrientationPatient]
    delx, dely = d.PixelSpacing

    xx = o0 * delx * x + o3 * dely * y + sx
    yy = o1 * delx * x + o4 * dely * y + sy
    zz = o2 * delx * x + o5 * dely * y + sz
    return xx,yy,zz

## read data #########################################################
def resize_volume(volume, image_size):
    image = volume.copy()
    image = np.ascontiguousarray(image.transpose((1, 2, 0)))
    image = cv2.resize(image, (image_size, image_size), interpolation=cv2.INTER_LINEAR)
    image = np.ascontiguousarray(image.transpose((2, 0, 1)))  # cv2.INTER_LINEAR=1
    return image

def normalise_to_8bit(x, lower=0.1, upper=99.9): # 1, 99 #0.05, 99.5 #0, 100
    lower, upper = np.percentile(x, (lower, upper))
    x = np.clip(x, lower, upper)
    x = x - np.min(x)
    x = x / np.max(x)
    return (x * 255).astype(np.uint8)
def read_series(study_id,series_id,series_description):
    data_kaggle_dir = DATA_KAGGLE_DIR
    dicom_dir = f'{data_kaggle_dir}/{train_test}_images/{study_id}/{series_id}'

    # read dicom file
    dicom_file = natsorted(glob.glob(f'{dicom_dir}/*.dcm'))
    instance_number = [int(f.split('/')[-1].split('.')[0]) for f in dicom_file]
    dicom = [pydicom.dcmread(f) for f in dicom_file]

    # make dicom header df
    H, W = dicom[0].pixel_array.shape
    dicom_df = []
    for i, d in zip(instance_number, dicom):  # d__.dict__
        dicom_df.append(
            dotdict(
                study_id=study_id,
                series_id=series_id,
                series_description=series_description,
                instance_number=i,
                # InstanceNumber = d.InstanceNumber,
                ImagePositionPatient=[float(v) for v in d.ImagePositionPatient],
                ImageOrientationPatient=[float(v) for v in d.ImageOrientationPatient],
                PixelSpacing=[float(v) for v in d.PixelSpacing],
                SpacingBetweenSlices=float(d.SpacingBetweenSlices),
                SliceThickness=float(d.SliceThickness),
                grouping=str([round(float(v), 3) for v in d.ImageOrientationPatient]),
                H=H,
                W=W,
            )
        )
    dicom_df = pd.DataFrame(dicom_df)

    # sort slices
    dicom_df = [d for _, d in dicom_df.groupby('grouping')]

    data = []
    sort_data_by_group = []
    for df in dicom_df:
        position = np.array(df['ImagePositionPatient'].values.tolist())
        orientation = np.array(df['ImageOrientationPatient'].values.tolist())
        normal = np.cross(orientation[:, :3], orientation[:, 3:])
        projection = np_dot(normal, position)
        df.loc[:, 'projection'] = projection
        df = df.sort_values('projection')


        # todo: assert all slices are continous ??
        # use  (position[-1]-position[0])/N = SpacingBetweenSlices ??
        assert len(df.SliceThickness.unique()) == 1
        assert len(df.SpacingBetweenSlices.unique()) == 1


        volume = [
            dicom[instance_number.index(i)].pixel_array for i in df.instance_number
        ]
        volume = np.stack(volume)
        volume = normalise_to_8bit(volume)
        data.append(dotdict(
            df=df,
            volume=volume,
        ))

        if 'sagittal' in series_description.lower():
            sort_data_by_group.append(position[0, 0])  # x
        if 'axial' in series_description.lower():
            sort_data_by_group.append(position[0, 2])  # z

    data = [r for _, r in sorted(zip(sort_data_by_group, data))]
    for i, r in enumerate(data):
        r.df.loc[:, 'group'] = i

    df = pd.concat([r.df for r in data])
    df.loc[:, 'z'] = np.arange(len(df))
    try:    
        volume = np.concatenate([r.volume for r in data])
    except:
        volume = []
        for r in data:
            # st()
            volume.append([cv2.resize(im, (608, 608)) for im in r.volume])
        volume = np.concatenate(volume)
    data = dotdict(
        series_id=series_id,
        df=df,
        volume=volume,
    )
    return data
def read_axial_df(study_id,series_id,series_description):
    data_kaggle_dir = DATA_KAGGLE_DIR
    dicom_dir = f'{data_kaggle_dir}/{train_test}_images/{study_id}/{series_id}'

    # read dicom file
    dicom_file = natsorted(glob.glob(f'{dicom_dir}/*.dcm'))
    instance_number = [int(f.split('/')[-1].split('.')[0]) for f in dicom_file]
    dicom = [pydicom.dcmread(f) for f in dicom_file]

    # make dicom header df
    H, W = dicom[0].pixel_array.shape
    dicom_df = []
    for i, d in zip(instance_number, dicom):  # d__.dict__
        dicom_df.append(
            dotdict(
                study_id=study_id,
                series_id=series_id,
                series_description=series_description,
                instance_number=i,
                # InstanceNumber = d.InstanceNumber,
                ImagePositionPatient=[float(v) for v in d.ImagePositionPatient],
                ImageOrientationPatient=[float(v) for v in d.ImageOrientationPatient],
                PixelSpacing=[float(v) for v in d.PixelSpacing],
                SpacingBetweenSlices=float(d.SpacingBetweenSlices),
                SliceThickness=float(d.SliceThickness),
                grouping=str([round(float(v), 3) for v in d.ImageOrientationPatient]),
                H=H,
                W=W,
            )
        )
    dicom_df = pd.DataFrame(dicom_df)

    # sort slices
    dicom_df = [d for _, d in dicom_df.groupby('grouping')]

    data = []
    sort_data_by_group = []
    for df in dicom_df:
        position = np.array(df['ImagePositionPatient'].values.tolist())
        orientation = np.array(df['ImageOrientationPatient'].values.tolist())
        normal = np.cross(orientation[:, :3], orientation[:, 3:])
        projection = np_dot(normal, position)
        df.loc[:, 'projection'] = projection
        df = df.sort_values('projection')


        # todo: assert all slices are continous ??
        # use  (position[-1]-position[0])/N = SpacingBetweenSlices ??
        assert len(df.SliceThickness.unique()) == 1
        if len(df.SpacingBetweenSlices.unique()) != 1:
            import pdb;pdb.set_trace()
        assert len(df.SpacingBetweenSlices.unique()) == 1


        volume = [
            dicom[instance_number.index(i)].pixel_array for i in df.instance_number
        ]
        volume = np.stack(volume)
        volume = normalise_to_8bit(volume)
        data.append(dotdict(
            df=df,
            volume=volume,
        ))

        if 'sagittal' in series_description.lower():
            sort_data_by_group.append(position[0, 0])  # x
        if 'axial' in series_description.lower():
            sort_data_by_group.append(position[0, 2])  # z

    data = [r for _, r in sorted(zip(sort_data_by_group, data))]
    for i, r in enumerate(data):
        r.df.loc[:, 'group'] = i

    df = pd.concat([r.df for r in data])
    df.loc[:, 'z'] = np.arange(len(df))
    return df

def read_study(study_id, sagittal_t2_id, axial_t2_id):
    return dotdict(
        study_id = study_id,
        sagittal_t2 =read_series(study_id, sagittal_t2_id, 'sagittal_t2'),
        axial_t2 =read_series(study_id, axial_t2_id, 'axial_t2'),
    )
def get_true_sagittal_t2_point(study_id, sagittal_t2_df):
    series_id = sagittal_t2_df.iloc[0].series_id
    label_coord_df = pd.read_csv(f'{DATA_KAGGLE_DIR}/{train_test}_label_coordinates.csv')
    label_df = label_coord_df[
         (label_coord_df.study_id == study_id)
       & (label_coord_df.series_id == series_id)
    ]
    label_df = label_df.sort_values('level')
    point=label_df[['x','y']].values
    instance_number = label_df.instance_number.values

    #mapping from instance num to z (array index)
    map_instance_number, map_z = sagittal_t2_df[['instance_number','z',]].values.T
    map = {n:z for n,z in zip(map_instance_number,map_z)}
    z = [map[n] for n in instance_number]
    return point,z

############################################################3
#post processing (sagittal_t2 point net)
def probability_to_point(probability, threshold=0.5):
    #todo: handle mssing point
    point=[]
    for l in range(1, 6):
        y, x = np.where(probability[l] > threshold)
        y = round(y.mean())
        x = round(x.mean())
        point.append((x, y))
    return point


def view_to_world(sagittal_t2_point, z, sagittal_t2_df, image_size):

    H = sagittal_t2_df.iloc[0].H
    W = sagittal_t2_df.iloc[0].W
    scale_x = W / image_size
    scale_y = H / image_size

    xxyyzz = []
    for l in range(1, 6):
        x,y = sagittal_t2_point[l-1]
        xx,yy,zz = project_to_3d(x*scale_x, y*scale_y, z, sagittal_t2_df)
        xxyyzz.append((xx, yy, zz))

    xxyyzz = np.array(xxyyzz)
    return xxyyzz

def point_to_level(world_point, axial_t2_df):

    # we get closest axial slices (z) to the CSC world points

    xxyyzz = world_point
    orientation = np.array(axial_t2_df.ImageOrientationPatient.values.tolist())
    position = np.array(axial_t2_df.ImagePositionPatient.values.tolist())
    ox = orientation[:, :3]
    oy = orientation[:, 3:]
    oz = np.cross(ox, oy)
    t = xxyyzz.reshape(-1, 1, 3) - position.reshape(1, -1, 3)
    dis = (oz.reshape(1, -1, 3) * t).sum(-1)  # np.dot(point-s,oz)
    fdis = np.fabs(dis)
    closest_z = fdis.argmin(-1)
    closest_fdis = fdis.min(-1)
    closest_df = axial_t2_df.iloc[closest_z]

    if 1:
        #<todo> hard/soft assigment, multi/single assigment
        # no assignment based on distance

        # allow point found in multi group
        num_group   = len(axial_t2_df['group'].unique())
        point_group = axial_t2_df.group.values[fdis.argsort(-1)[:, :3]].tolist()
        point_group = [list(set(g)) for g in point_group]
        group_point = [[] for g in range(num_group)]
        for l in range(5):
            for k in point_group[l]:
                group_point[k].append(l)
                # print(k)
                # print(group_point[k])
                # print(group_point)
        group_point = [sorted(list(set(g))) for g in group_point]

    D = len(axial_t2_df)
    assigned_level=np.full(D,fill_value=0, dtype=int)
    for group in range(num_group):
        point_in_this_group = np.array(group_point[group])  # np.where(closest_df['group'] == group)[0]
        slice_in_this_group = np.where(axial_t2_df['group'] == group)[0]
        if len(point_in_this_group) == 0:
            continue # unassigned, level=0

        level = point_in_this_group[fdis[point_in_this_group][:, slice_in_this_group].argmin(0)] + 1
        assigned_level[slice_in_this_group] = level

    # sor =  (fdis.argmin(0)+1)[closest_z]
    # closest_z= [ fdis.argmin(0)+1]
    return assigned_level, closest_z, closest_fdis #dis is soft assignment


#########################################################################3
#visualisation
level_color = [
    [0, 0, 0],
    [255, 0, 0],
    [0, 255, 0],
    [0, 0, 255],
    [255, 255, 0],
    [0, 255, 255],
]

def probability_to_rgb(probability):
    _6_,H,W = probability.shape
    rgb = np.zeros((H, W, 3))
    for i in range(1, 6):
        rgb += probability[i].reshape(H, W, 1) * [[level_color[i]]]
    rgb = rgb.astype(np.uint8)
    return rgb


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        return np.min(zs)

def draw_slice(
    ax, df,
    is_slice =True, scolor=[[1,0,0]], salpha=[0.1],
    is_border=True, bcolor=[[1,0,0]], balpha=[0.1],
    is_origin=True, ocolor=[[1,0,0]], oalpha=[0.1],
    is_arrow=True,
):
    df = df.copy()
    df = df.reset_index(drop=True)

    D = len(df)
    if len(scolor)==1: scolor = scolor*D
    if len(salpha)==1: salpha = salpha*D
    if len(bcolor)==1: bcolor = bcolor*D
    if len(balpha)==1: balpha = balpha*D
    if len(ocolor)==1: ocolor = bcolor*D
    if len(oalpha)==1: oalpha = balpha*D


    #for i,d in df.iterrows():
    for i in range(D):
        d = df.iloc[i]
        W, H = d.W, d.H
        o0, o1, o2, o3, o4, o5 = d.ImageOrientationPatient
        ox = np.array([o0, o1, o2])
        oy = np.array([o3, o4, o5])
        sx, sy, sz = d.ImagePositionPatient
        s = np.array([sx, sy, sz])
        delx, dely = d.PixelSpacing

        p0 = s
        p1 = s + W * delx * ox
        p2 = s + H * dely * oy
        p3 = s + H * dely * oy + W * delx * ox

        grid = np.stack([p0, p1, p2, p3]).reshape(2, 2, 3)
        gx = grid[:, :, 0]
        gy = grid[:, :, 1]
        gz = grid[:, :, 2]

        #outline
        if is_slice:
            ax.plot_surface(gx, gy, gz, color=scolor[i], alpha=salpha[i])

        if is_border:
            line = np.stack([p0, p1, p3, p2] )
            ax.plot(line[:,0], line[:,1], zs=line[:,2], color=ocolor[i], alpha=oalpha[i])

        if is_origin:
            ax.scatter([sx], [sy], [sz],   color=ocolor[i], alpha=oalpha[i])

    #check ordering of slice
    if is_arrow :
        sx0, sy0, sz0 = df.iloc[0].ImagePositionPatient
        sx1, sy1, sz1 = df.iloc[-1].ImagePositionPatient
        arrow_prop_dict = dict(mutation_scale=20, arrowstyle='-|>', color='k', shrinkA=0, shrinkB=0)
        a = Arrow3D([sx0, sx1], [sy0, sy1], [sz0, sz1], **arrow_prop_dict)
        ax.add_artist(a)


plot = False        


from tqdm import tqdm
dfs = []
error_ids = []
all_dfs = []
for study_id_n, study_id in enumerate(tqdm(id_df.study_id.unique())):
    for axial_t2_id in id_df[(id_df.study_id == study_id) & (id_df.series_description=='Axial T2')].series_id.values:
        try:

            sagittal_t2_id = id_df[(id_df.study_id == study_id) & (id_df.series_description=='Sagittal T2/STIR')].iloc[0].series_id
            data = read_study(study_id, axial_t2_id=axial_t2_id, sagittal_t2_id=sagittal_t2_id)


            #--- step.1 : detect 2d point in sagittal_t2
            sagittal_t2 = data.sagittal_t2.volume
            sagittal_t2_df = data.sagittal_t2.df
            axial_t2_df = data.axial_t2.df
            all_dfs.append(axial_t2_df)

            D,H,W = sagittal_t2.shape
            image = resize_volume(sagittal_t2,cfg.point_net.image_size)

            sagittal_t2_z = D//2
            image = image[sagittal_t2_z] #we use only center image #todo: better selection

            batch = dotdict(
                sagittal=torch.from_numpy(image).unsqueeze(0).unsqueeze(0).byte()
            )
            with torch.cuda.amp.autocast(enabled=True):
                with torch.no_grad():
                    output = point_net(batch)

            probability = output['probability'][0].float().data.cpu().numpy()
            sagittal_t2_point = probability_to_point(probability) #5 level 2d points, todo: check invalid output point

#             #for debug and development
#             point_hat, z_hat = sagittal_t2_point_hat = get_true_sagittal_t2_point(study_id, sagittal_t2_df)
#             point_hat = point_hat*[[cfg.point_net.image_size/W, cfg.point_net.image_size/H]]


            #--- step.2 : perdict slice level of axial_t2
            world_point = world_point = view_to_world(sagittal_t2_point, sagittal_t2_z, sagittal_t2_df, cfg.point_net.image_size)
            assigned_level, closest_z, closest_fdis = axial_t2_level = point_to_level(world_point, axial_t2_df)
            
            axial_t2_df['level'] = assigned_level
#             break
            exist_closest_fdis = closest_fdis[np.unique([c for c in assigned_level if c != 0])-1]
            exist_closest_z = closest_z[np.unique([c for c in assigned_level if c != 0])-1]
            ns = axial_t2_df.iloc[exist_closest_z].instance_number    
            axial_t2_df.loc[~axial_t2_df.instance_number.isin(ns), 'closest'] = 0
            axial_t2_df.loc[axial_t2_df.instance_number.isin(ns), 'closest'] = 1
            axial_t2_df['closest'] = axial_t2_df['closest'].astype(int)
            for level in range(1, 6):
                axial_t2_df.loc[axial_t2_df.level == level, 'dis'] = closest_fdis[level-1]            
                
            for n, dis in zip(ns, exist_closest_fdis):
                axial_t2_df.loc[axial_t2_df.instance_number == n, 'dis'] = dis
                
            assert len(assigned_level)==len(axial_t2_df)
            dfs.append(axial_t2_df)        



            if plot:
#             if exist_closest_fdis.max() > 5:                
                print(axial_t2_id, exist_closest_fdis.max(), assigned_level)
                ###################################################################
                #visualisation

                # https://matplotlib.org/stable/gallery/mplot3d/mixed_subplots.html
                fig = plt.figure(figsize=(23, 6))
                ax1 = fig.add_subplot(1, 1, 1)
                ax2 = fig.add_subplot(1, 2, 2, projection='3d')

                # detection result
                p = probability_to_rgb(probability)
                m = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
                m = 255 - (255 - m * 0.8) * (1 - p / 255)

                ax1.imshow(m / 255)
                ax1.set_title(f'sagittal keypoint detection (unet)\n series_id: {axial_t2_id}')


                # draw  assigned_level
                level_ncolor = np.array(level_color) / 255
                coloring = level_ncolor[assigned_level].tolist()
                draw_slice(
                    ax2, axial_t2_df,
                    is_slice=True,   scolor=coloring, salpha=[0.1],
                    is_border=True,  bcolor=coloring, balpha=[0.2],
                    is_origin=False, ocolor=[[0, 0, 0]], oalpha=[0.0],
                    is_arrow=True
                )

            #     draw world_point
                ax2.scatter(world_point[:, 0], world_point[:, 1], world_point[:, 2], alpha=1, color='black')


                ### draw closest slice
                coloring = level_ncolor[1:].tolist()
                draw_slice(
                    ax2, axial_t2_df.iloc[closest_z],
                    is_slice=True, scolor=coloring, salpha=[0.1],
                    is_border=True, bcolor=coloring, balpha=[1],
                    is_origin=False, ocolor=[[1, 0, 0]], oalpha=[0],
                    is_arrow=False
                )

                ax2.set_aspect('equal')
                ax2.set_title(f'axial slice assignment\n series_id:{sagittal_t2_id}')
                ax2.set_xlabel('x')
                ax2.set_ylabel('y')
                ax2.set_zlabel('z')
                ax2.view_init(elev=0, azim=-10, roll=0)
                plt.tight_layout(pad=2)
                plt.show()
    
        except:
            error_ids.append(axial_t2_id)
axial_closest_df = pd.concat(dfs)
axial_direction = pd.concat(all_dfs)
axial_direction.to_csv('axial_direction.csv', index=False)
axial_closest_df.to_csv('axial_closest_df.csv', index=False)


# # 2, setup

# In[ ]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from glob import glob
import albumentations as A
import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import copy
from scipy.special import softmax
def sigmoid(x):
    return 1/(1 + np.exp(-x))
from sklearn.metrics import roc_auc_score, confusion_matrix, mean_squared_error, average_precision_score, recall_score
import warnings
warnings.simplefilter('ignore')

import os
import cv2
import gdcm
import pydicom
import zipfile
import seaborn as sns
import matplotlib.pyplot as plt
import dicomsdl
from pdb import set_trace as st
from tqdm import tqdm
from joblib import Parallel, delayed
from pydicom.pixel_data_handlers.util import apply_voi_lut
import torch

# In[ ]:


def standardize_pixel_array(dcm: pydicom.dataset.FileDataset) -> np.ndarray:
    """
    Source : https://www.kaggle.com/competitions/rsna-2023-abdominal-trauma-detection/discussion/427217
    """
    # Correct DICOM pixel_array if PixelRepresentation == 1.
    pixel_array = dcm.pixel_array
    if dcm.PixelRepresentation == 1:
        bit_shift = dcm.BitsAllocated - dcm.BitsStored
        dtype = pixel_array.dtype 
        new_array = (pixel_array << bit_shift).astype(dtype) >>  bit_shift
        pixel_array = pydicom.pixel_data_handlers.util.apply_modality_lut(new_array, dcm)
    return pixel_array

def get_center_x_path(study_id, series_id):
    path_x_map = {}
    for dcm_path in sorted(glob(f"{dicom_dir}/{study_id}/{series_id}/*.dcm")):
        filename = dcm_path.split('/')[-1].replace('.dcm', '')
    #         if int(instance_number) % 2 == 1:
    #             continue
        dicom = dicomsdl.open(dcm_path)
        pos_x = dicom['ImagePositionPatient'][0]
        path_x_map[pos_x] = dcm_path
        xs = []
        for i, k in enumerate(sorted(path_x_map.keys())):
            xs.append(k)
    return path_x_map[xs[len(xs)//2-1]], path_x_map[xs[len(xs)//2]], path_x_map[xs[len(xs)//2+1]]

def read_sagittal_x_center_dicom(args, verbose=False):
    study_id, series_id = args
    ch_imgs = []
    dcm_path_3 = get_center_x_path(study_id, series_id)
    for dcm_path in dcm_path_3:
        dicom = dicomsdl.open(dcm_path)
        img = dicom.pixelData(storedvalue = True)

        if dicom['PixelRepresentation'] == 1:
            bit_shift = dicom['BitsAllocated'] - dicom['BitsStored']
            dtype = img.dtype
            img = (img << bit_shift).astype(dtype) >>  bit_shift
        img = img.astype(np.float32)

        intercept = dicom['RescaleIntercept']
        slope = dicom['RescaleSlope']
        if (slope is not None) & (intercept is not None):
            img = img * slope + intercept

        img = (img - img.min()) / (img.max() - img.min() + 1e-6)

        if dicom.PhotometricInterpretation == "MONOCHROME1":
            img = 1 - img
        img = (img*255.0).astype('uint8')

        ch_imgs.append(img)
    if verbose:
        plt.imshow(ch_imgs[1], 'gray')
        plt.show()
    img = np.array(ch_imgs).transpose((1,2,0))
    cv2.imwrite(f'/kaggle/temp/sagittal_all_images/{study_id}___{series_id}.png', img)
    
    
    
def select_path_list(lst, N, offset=0, skip=1):
    if not lst:
        return [''] * (2 * N + 1)
    
    center = (len(lst) // 2) + offset
    result = [''] * (2 * N + 1)
    
    if 0 <= center < len(lst):
        result[N] = lst[center]
    
    for i in range(1, N + 1):
        left_index = center - i*skip
        right_index = center + i*skip
        
        if 0 <= left_index < len(lst):
            result[N - i] = lst[left_index]
        else:
            result[N - i] = lst[0]
        if 0 <= right_index < len(lst):
            result[N + i] = lst[right_index]
        else:
            result[N + i] = lst[len(lst)-1]
    
    return result

    
def read_sagittal_dicom(args, verbose=False):
    study_id, series_id = args
    imgs = {}
    origin_paths = []
    zs = []
    xyzs = []
    paths = []
    for dcm_path in glob(f"{dicom_dir}/{study_id}/{series_id}/*.dcm"):
        filename = dcm_path.split('/')[-1].replace('.dcm', '')
        dicom = dicomsdl.open(dcm_path)
        img = dicom.pixelData(storedvalue = True)

        if dicom['PixelRepresentation'] == 1:
            bit_shift = dicom['BitsAllocated'] - dicom['BitsStored']
            dtype = img.dtype
            img = (img << bit_shift).astype(dtype) >>  bit_shift
        img = img.astype(np.float32)

        intercept = dicom['RescaleIntercept']
        slope = dicom['RescaleSlope']
        if (slope is not None) & (intercept is not None):
            img = img * slope + intercept

        img = (img - img.min()) / (img.max() - img.min() + 1e-6)

        if dicom.PhotometricInterpretation == "MONOCHROME1":
            img = 1 - img
        img = (img*255.0).astype('uint8')
        save_path = f'/kaggle/temp/sagittal_all_images/{study_id}___{series_id}___{filename}.png'
        paths.append(save_path)

        imgs[save_path] = img
        origin_paths.append(dcm_path)
        xyzs.append(dicom['ImagePositionPatient'])

    df = pd.DataFrame({
        'path': paths,
        'origin_path': origin_paths,
    })
    df[['x_pos', 'y_pos', 'z_pos']] = np.array(xyzs)
    df['study_id'] = study_id
    df['series_id'] = series_id
    df['instance_number'] = df['path'].apply(lambda x: int(x.split('___')[-1].replace('.png', '')))
    df = df.sort_values(['x_pos', 'instance_number'])
    df = df.drop_duplicates('x_pos')        
    path_list = df.path.values
    for path_n, path in enumerate(df.path):
        if path_n == 0:
            prev_path = df.path.values[0]
        else:
            prev_path = df.path.values[path_n-1]
        prev_im = imgs[prev_path]            
        
        im = imgs[path]
        if path_n == len(df)-1:
            next_path = df.path.values[-1]
        else:
            next_path = df.path.values[path_n+1]
        next_im = imgs[next_path]
  
        if not (prev_im.shape == im.shape == next_im.shape):
            s = prev_im.shape
            im = cv2.resize(im, s)
            next_im = cv2.resize(next_im, s)

        image = np.array([prev_im, im, next_im]).transpose((1,2,0))
        cv2.imwrite(path, image)
    
    if verbose:
        rows = 7
        for n, k in enumerate(sorted(imgs.keys())):
            if n % rows == 0:
                fig = plt.figure(figsize=(20, 20))
            fig.add_subplot(1, rows, n%rows+1)

            im = imgs[k]
            plt.imshow(im, 'gray')

            if n % rows == rows-1:
                plt.show()        
        
    return df

def read_axial_dicom(args, verbose=False):
    study_id, series_id = args
    imgs = {}
    origin_paths = []
    zs = []
    xyzs = []
    paths = []
    series_axial_direction = axial_direction[axial_direction.series_id==series_id]
    for dcm_path in glob(f"{dicom_dir}/{study_id}/{series_id}/*.dcm"):
        filename = dcm_path.split('/')[-1].replace('.dcm', '')
#         if int(instance_number) % 2 == 1:
#             continue
        dicom = dicomsdl.open(dcm_path)
        img = dicom.pixelData(storedvalue = True)

        if dicom['PixelRepresentation'] == 1:
            bit_shift = dicom['BitsAllocated'] - dicom['BitsStored']
            dtype = img.dtype
            img = (img << bit_shift).astype(dtype) >>  bit_shift
        img = img.astype(np.float32)

        intercept = dicom['RescaleIntercept']
        slope = dicom['RescaleSlope']
        if (slope is not None) & (intercept is not None):
            img = img * slope + intercept

        pos_z = dicom['ImagePositionPatient'][-1]
        
        img = (img - img.min()) / (img.max() - img.min() + 1e-6)

        if dicom.PhotometricInterpretation == "MONOCHROME1":
            img = 1 - img
        img = (img*255.0).astype('uint8')
        save_path = f'/kaggle/temp/axial_all_images/{study_id}___{series_id}___{filename}.png'
        paths.append(save_path)

        imgs[save_path] = img
        origin_paths.append(dcm_path)
        xyzs.append(dicom['ImagePositionPatient'])

    df = pd.DataFrame({
        'path': paths,
        'origin_path': origin_paths,
    })
    df[['x_pos', 'y_pos', 'z_pos']] = np.array(xyzs)
    df['study_id'] = study_id
    df['series_id'] = series_id
    df['instance_number'] = df['path'].apply(lambda x: int(x.split('___')[-1].replace('.png', '')))

    l = len(df)
    if len(df.merge(series_axial_direction[['instance_number', 'z']], on='instance_number')) == l:
        df = df.merge(series_axial_direction[['instance_number', 'z']], on='instance_number')
        df = df.sort_values(['z', 'instance_number'])
    else:
        df = df.sort_values(['z_pos', 'instance_number'])
    path_list = df.path.values

    for path_n, path in enumerate(df.path):
        im = imgs[path]
        if path_n == 0:
            prev_path = df.path.values[0]
        else:
            prev_path = df.path.values[path_n-1]
        prev_im = imgs[prev_path]
        
        if path_n == len(df)-1:
            next_path = df.path.values[-1]
        else:
            next_path = df.path.values[path_n+1]
        next_im = imgs[next_path]
  
        if not (prev_im.shape == im.shape == next_im.shape):

            s = prev_im.shape
            im = cv2.resize(im, s)
            next_im = cv2.resize(next_im, s)

        image = np.array([prev_im, im, next_im]).transpose((1,2,0))
        cv2.imwrite(path, image)

    if series_id not in axial_closest_df.series_id.unique():
        for path_n, path in enumerate(df.path):
            im = imgs[path]
            if path_n <= 1:
                prev_path = df.path.values[0]
            else:
                prev_path = df.path.values[path_n-2]
            prev_im = imgs[prev_path]
            
            if path_n >= len(df)-2:
                next_path = df.path.values[-1]
            else:
                next_path = df.path.values[path_n+2]
            next_im = imgs[next_path]
      
            if not (prev_im.shape == im.shape == next_im.shape):

                s = prev_im.shape
                im = cv2.resize(im, s)
                next_im = cv2.resize(next_im, s)

            image = np.array([prev_im, im, next_im]).transpose((1,2,0))
            cv2.imwrite(path.replace('.png', '_stride2.png'), image)

        for path_n, path in enumerate(df.path):
            im = imgs[path]
            if path_n <= 2:
                prev_path = df.path.values[0]
            else:
                prev_path = df.path.values[path_n-3]
            prev_im = imgs[prev_path]
            
            if path_n >= len(df)-3:
                next_path = df.path.values[-1]
            else:
                next_path = df.path.values[path_n+3]
            next_im = imgs[next_path]
      
            if not (prev_im.shape == im.shape == next_im.shape):

                s = prev_im.shape
                im = cv2.resize(im, s)
                next_im = cv2.resize(next_im, s)

            image = np.array([prev_im, im, next_im]).transpose((1,2,0))
            cv2.imwrite(path.replace('.png', '_stride3.png'), image)
        
    if verbose:
        rows = 7
        for n, k in enumerate(sorted(imgs.keys())):
            if n % rows == 0:
                fig = plt.figure(figsize=(20, 20))
            fig.add_subplot(1, rows, n%rows+1)

            im = imgs[k]
            plt.imshow(im, 'gray')

            if n % rows == rows-1:
                plt.show()        
        
    return df


# In[ ]:


DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

use_local_box_when_debug = False

if debug:
    df = pd.read_csv('/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification/train_series_descriptions.csv')
    fold_df = pd.read_csv('/kaggle/input/rsna2024-csvs/train_v3.csv')
    df = df[df.study_id.isin(fold_df[fold_df.fold==debug_fold].study_id)]
    if short_debug:
        df = df[df.study_id.isin(use_ids)]
#         df = df[df.series_id==3636216534]

else:
    df = pd.read_csv('/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification/test_series_descriptions.csv')
dicom_dir = f'/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification/{train_test}_images'


# # dicom to png

# In[ ]:



image_save_dir = '/kaggle/temp/axial_all_images'
os.makedirs(image_save_dir, exist_ok=True)

axial_df = df[df.series_description == 'Axial T2']
args = axial_df.drop_duplicates(['study_id', 'series_id'])[['study_id', 'series_id']].values


from multiprocessing import Pool

p = Pool(processes=4)
results = []
with tqdm(total=len(args)) as pbar:
    for res in p.imap(read_axial_dicom, args):
        results.append(res)
        pbar.update(1)
p.close()

axial_df = pd.concat(results)
axial_df.to_csv('axial_df.csv', index=False)

image_save_dir = '/kaggle/temp/sagittal_all_images'
os.makedirs(image_save_dir, exist_ok=True)

sagittal_df = df[df.series_description != 'Axial T2']
args = sagittal_df.drop_duplicates(['study_id', 'series_id'])[['study_id', 'series_id']].values

from multiprocessing import Pool

p = Pool(processes=4)
results = []
with tqdm(total=len(args)) as pbar:
    for res in p.imap(read_sagittal_dicom, args):
        results.append(res)
        pbar.update(1)
p.close()

sagittal_df = pd.concat(results)
sagittal_df.to_csv('sagittal_df.csv', index=False)

sagittal_df = pd.read_csv('sagittal_df.csv')
series_description_df = pd.read_csv(f'/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification/{train_test}_series_descriptions.csv')
sagittal_df = sagittal_df.merge(series_description_df, on=['study_id', 'series_id'])

for study_id_n, (study_id, idf) in enumerate(tqdm(sagittal_df.groupby('study_id'))):
    t1 = idf[idf.series_description=='Sagittal T1'].sort_values('instance_number')
    if len(t1)!=0:
        t1 = t1[t1.series_id==t1.series_id.values[0]]
    t2 = idf[idf.series_description=='Sagittal T2/STIR'].sort_values('instance_number')
    if len(t2)!=0:
        t2 = t2[t2.series_id==t2.series_id.values[0]]
    if len(t1)==0:
        m = t2.instance_number.max()
        mi = t2.instance_number.min()
    elif (len(t2)==0):
        m = t1.instance_number.max()
        mi = t1.instance_number.min()
    else:
        m = max([t1.instance_number.max(), t2.instance_number.max()])
        mi = min([t1.instance_number.min(), t2.instance_number.min()])
    for n in range(mi, m+1):
        n1 = t1[t1.instance_number == n]
        n2 = t2[t2.instance_number == n]
        if len(n1) != 0:
            # print(n1.path.values[0])
            im1 = cv2.imread(n1.path.values[0])[:,:,1]
        else:
            im1 = None
        if len(n2) != 0:
            # print(n2.path.values[0])
            im2 = cv2.imread(n2.path.values[0])[:,:,1]
        else:
            im2 = None
        if im1 is None:
            # raise
            im1 = np.zeros(im2.shape)
        if im2 is None:
            # raise
            im2 = np.zeros(im1.shape)
        if im1.shape!=im2.shape:
            im1 = cv2.resize(im1, (im2.shape[1], im2.shape[0]))
        im = np.array([im1, im2, im1]).transpose((1,2,0))

        cv2.imwrite(f'/kaggle/temp/sagittal_all_images/{study_id}___{n}.png', im)


# In[ ]:


axial_closest_df = axial_closest_df[axial_closest_df.closest==1]
axial_closest_df['pred_level'] = axial_closest_df.level.values
axial_closest_df['path'] = '/kaggle/temp/axial_all_images/' + axial_closest_df.study_id.astype(str) + '___' + axial_closest_df.series_id.astype(str) + '___' + axial_closest_df.instance_number.astype(str) + '.png'
axial_closest_df['level_pred'] = 1
axial_closest_df[['study_id', 'series_id', 'path', 'level_pred', 'pred_level', 'instance_number', 'z']]
axial_all_level_df = axial_closest_df[['study_id', 'series_id', 'path', 'level_pred', 'pred_level', 'instance_number', 'z', 'dis']]
axial_all_level_df.to_csv('axial_all_level_df.csv', index=False)

# # 4, spinal slice / nfn slice classification for sagittal

# In[ ]:


import albumentations as A
from albumentations.pytorch import ToTensorV2
import timm

class RSNA2024DatasetV1(Dataset):
    def __init__(self, cfg):
        self.transforms = cfg.transforms
        self.cfg = cfg
        self.paths = cfg.df.path.values
        if 'x_min' in list(cfg.df):
            self.boxes = cfg.df[['x_min', 'y_min', 'x_max', 'y_max']].values
    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        path = self.paths[idx]
        image = cv2.imread(path)[:,:,::-1]

        if hasattr(self.cfg, 'box_crop') and self.cfg.box_crop:
            box = self.boxes[idx]
            x_pad = (box[2] - box[0])//2 * self.cfg.box_crop_x_ratio
            y_pad = (box[3] - box[1])//2 * self.cfg.box_crop_y_ratio
            x_min = np.max([box[0]-x_pad, 0])
            y_min = np.max([box[1]-y_pad, 0])
            if hasattr(self.cfg, 'box_crop_y_upper_ratio'):
                y_upper_pad = (box[3] - box[1])//2 * self.cfg.box_crop_y_upper_ratio
                y_min = np.max([box[1]-y_upper_pad, 0])
            x_max = np.min([box[2]+x_pad, image.shape[1]])
            y_max = np.min([box[3]+y_pad, image.shape[0]])
            s = image.shape
            image = image[int(y_min):int(y_max), int(x_min):int(x_max), :]
            # print(s, image.shape)

        image = self.transforms(image=image)['image']

        return image

class base():
    def __init__(self):
        self.model_name = 'convnext_small.in12k_ft_in1k_384'
        self.image_size = 384
        self.batch_size = 16
        self.tta = False
        self.box_crop = None
        self.transforms = A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(),
            ToTensorV2(),
        ])
        
class rsna_sagittal_cl(base):
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv('sagittal_df.csv')
        self.label_features = ['l1_spinal', 'l2_spinal', 'l3_spinal', 'l4_spinal', 'l5_spinal',
                               'l1_right_neural', 'l2_right_neural', 'l3_right_neural', 'l4_right_neural', 'l5_right_neural',
                               'l1_left_neural', 'l2_left_neural', 'l3_left_neural', 'l4_left_neural', 'l5_left_neural']
        self.image_size = 256
        
        d = '/kaggle/input/rsna-2024-sagittal-models-v1/rsna-sagittal-level-cl-spinal-nfn-v2'
        self.model = timm.create_model(self.model_name, pretrained=False, num_classes=len(self.label_features))
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.transforms = A.Compose([
            A.Compose([
                A.Resize(self.image_size, self.image_size),
                A.Normalize(),
                ToTensorV2(),
            ])
        ])              



# In[ ]:


all_preds = []
for cfg in [
    rsna_sagittal_cl(),
]:
    models = []
    for model_path in cfg.model_paths:
        # print(model_path)
        state_dict = torch.load(model_path, map_location=torch.device('cpu'))
        model = copy.deepcopy(cfg.model)
        model.load_state_dict(state_dict)
        model.to(DEVICE)
        model.eval()
        models.append(model)

    ds = RSNA2024DatasetV1(cfg)
    loader = DataLoader(ds, batch_size=cfg.batch_size, shuffle=False, drop_last=False, num_workers=4)
    preds = []
    for images in tqdm(loader, smoothing=0):
        images = images.to(DEVICE)
        batch_preds = []
        for model in models:
            batch_preds.append(model(images).detach().cpu().numpy())

        preds += np.mean(batch_preds, axis=0).tolist()
    all_preds.append(preds)
fs = [f'pred_{col}' for col in cfg.label_features]
cfg.df[fs] = sigmoid(np.mean(all_preds, 0))
cfg.df.to_csv(f'sagittal_with_position_preds.csv', index=False)


sagittal = cfg.df.copy()
sagittal['pred_spinal'] = sagittal[['pred_l1_spinal', 'pred_l2_spinal', 'pred_l3_spinal', 'pred_l4_spinal', 'pred_l5_spinal']].mean(1)
sagittal['pred_right_neural'] = sagittal[['pred_l1_right_neural', 'pred_l2_right_neural', 'pred_l3_right_neural', 'pred_l4_right_neural', 'pred_l5_right_neural']].mean(1)
sagittal['pred_left_neural'] = sagittal[['pred_l1_left_neural', 'pred_l2_left_neural', 'pred_l3_left_neural', 'pred_l4_left_neural', 'pred_l5_left_neural']].mean(1)


series_description_df = pd.read_csv(f'/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification/{train_test}_series_descriptions.csv')
t2_ids = series_description_df[series_description_df.series_description=='Sagittal T2/STIR'].series_id

dfs = []
for id, idf in sagittal[sagittal.series_id.isin(t2_ids)].groupby('series_id'):
    idf = idf.sort_values(['x_pos', 'instance_number'])
    idf = idf.drop_duplicates('x_pos')
    ldf = idf[idf['pred_spinal']==idf['pred_spinal'].max()].iloc[:1]
    dfs.append(ldf)

spinal_sagittal = pd.concat(dfs)
sagittal.to_csv('sagittal_df.csv', index=False)
spinal_sagittal.to_csv('spinal_sagittal_df.csv', index=False)
spinal_sagittal.study_id.nunique(), spinal_sagittal.series_id.nunique()


# # yolox

# In[ ]:


box_cols = ['x_min', 'y_min', 'x_max','y_max']
yolo_for_config_dir = '/kaggle/input/rsna-2024-axial-models-v1/rsna-axial-all-images-left-yolox-x'

yolo_for_config = 'rsna_axial_all_images_left_yolox_x'

import sys
sys.path.append('/kaggle/input/yolox20230421/YOLOX')

from yolox.utils import postprocess
from yolox.data.data_augment import ValTransform


class MyDataset(Dataset):
    def __init__(self, df):
        self.paths = df.path.values
        self.preproc = ValTransform(legacy = False)
        self.size = 512

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        path = self.paths[idx]
        img = cv2.imread(path)
        ratio = min(self.size / img.shape[0], self.size / img.shape[1])

        img, _ = self.preproc(img, None, (self.size, self.size))
        img = torch.from_numpy(img).float()
        img = img.float()

        return img, path, ratio

from yolox.exp import Exp as MyExp

class ExpX(MyExp):
    def __init__(self):
        super(ExpX, self).__init__()
        self.depth = 1.33
        self.width = 1.25
        self.exp_name = ''
        self.data_dir = ""

        ### need change ###
        self.max_epoch = 10
        self.output_dir = "."
        self.input_size = (512, 512)
        self.test_size = (512, 512)
        self.no_aug_epochs = 10 # 15
        self.warmup_epochs = 5 # 5
        self.num_classes = 1
        ### need change ###

        ### fyi ###
        self.data_num_workers = 16
        self.eval_interval = 1
        self.seed = 42
        self.print_interval = 100000
        self.eval_interval = 1
        self.save_history_ckpt = False
        self.mosaic_prob = 1.0
        self.mixup_prob = 1.0
        self.hsv_prob = 1.0
        self.flip_prob = 0.5
        self.degrees = 10.0
        self.translate = 0.1
        self.mosaic_scale = (0.1, 2)
        self.enable_mixup = True
        self.mixup_scale = (0.5, 1.5)
        self.shear = 2.0
        self.min_lr_ratio = 0.05
        self.basic_lr_per_img = 0.00015625
        self.scheduler = 'yoloxwarmcos'
        self.ema = True
        self.weight_decay = 0.0005
        self.momentum = 0.9
        self.test_conf = 0.01
        self.nmsthre = 0.65
        self.class_id_name_map = {0: 'left'}

class ExpL(MyExp):
    def __init__(self):
        super(ExpL, self).__init__()
        self.depth = 1.0
        self.width = 1.0
        self.exp_name = ''
        self.data_dir = ""

        ### need change ###
        self.max_epoch = 10
        self.output_dir = "."
        self.input_size = (512, 512)
        self.test_size = (512, 512)
        self.no_aug_epochs = 10 # 15
        self.warmup_epochs = 5 # 5
        self.num_classes = 1
        ### need change ###

        ### fyi ###
        self.data_num_workers = 16
        self.eval_interval = 1
        self.seed = 42
        self.print_interval = 100000
        self.eval_interval = 1
        self.save_history_ckpt = False
        self.mosaic_prob = 1.0
        self.mixup_prob = 1.0
        self.hsv_prob = 1.0
        self.flip_prob = 0.5
        self.degrees = 10.0
        self.translate = 0.1
        self.mosaic_scale = (0.1, 2)
        self.enable_mixup = True
        self.mixup_scale = (0.5, 1.5)
        self.shear = 2.0
        self.min_lr_ratio = 0.05
        self.basic_lr_per_img = 0.00015625
        self.scheduler = 'yoloxwarmcos'
        self.ema = True
        self.weight_decay = 0.0005
        self.momentum = 0.9
        self.test_conf = 0.01
        self.nmsthre = 0.65
        self.class_id_name_map = {0: 'left'}

exp_x = ExpX()

# set inference parameters
confthre = 0.03
nmsthre = 0.45

# get YOLOX model
models = []
for fold in range(1):
    model = exp_x.get_model()
    model.to(DEVICE)
    model.eval()
    model.head.training=False
    model.training=False
    ckpt_file = "/kaggle/input/notebookfa5fb155d5/rsna-axial-all-images-left-yolox-x/0_best_ckpt.ckpt"
    # print(ckpt_file)
    ckpt = torch.load(ckpt_file, map_location="cpu")
    model.load_state_dict(ckpt["model"])
    models.append(model)

ds = MyDataset(axial_all_level_df)
loader = DataLoader(ds, batch_size=16, shuffle=False, drop_last=False, num_workers=4)

all_preds_list = [[]]
all_ratios_list = [[]]
all_paths_list = [[]]

# print('inf start...')
with torch.no_grad():
    for loader_n, input in tqdm(enumerate(loader)):
        # if loader_n % 100 == 0:
        #     print(loader_n)
        images, paths, ratios = input
        images = images.to(DEVICE)
        for model_n, model in enumerate(models):
            outputs = model(images)
#             outputs2 = postprocess(
#                         outputs, exp_x.num_classes, confthre,
#                         nmsthre, class_agnostic=True
#                     )
            
#             st()
            
            outputs = postprocess(
                        outputs, exp_x.num_classes, confthre,
                        nmsthre, class_agnostic=True
                    )
            all_preds_list[model_n] += outputs
            all_ratios_list[model_n] += list(ratios)
            all_paths_list[model_n] += list(paths)

df_5models = []
for model_n, (all_preds, all_paths, all_ratios) in enumerate(zip(all_preds_list, all_paths_list, all_ratios_list)):
    dfs = []
    all_boxes = []
    all_class_ids = []
    all_scores = []
    for n, (predictions, path, ratio)  in enumerate(zip(all_preds, all_paths, all_ratios)):
        if predictions is None:
            continue
        predictions = predictions.cpu().numpy()

        bboxes = predictions[:, 0:4]

        bboxes /= ratio
        bboxes = bboxes.tolist()
        bbclasses = predictions[:, 6]
        scores = predictions[:, 4] * predictions[:, 5]
        path_df = axial_all_level_df[axial_all_level_df.path==path].iloc[:1]
        for box, score, class_id in zip(bboxes, scores, bbclasses):
            all_boxes.append(box)
            all_scores.append(score)
            all_class_ids.append(class_id)
            dfs.append(path_df)
    tmp = pd.concat(dfs)
    tmp['class_id'] = all_class_ids
    tmp['class_id'] = tmp['class_id'].astype(int)
    tmp['class_name'] = tmp['class_id'].map(exp_x.class_id_name_map)
    tmp['conf'] = all_scores
    tmp[box_cols] = all_boxes
    tmp[box_cols] = np.round(tmp[box_cols]).astype(int)
    tmp['model_n'] = model_n
    df_5models.append(tmp)

from ensemble_boxes import *
from multiprocessing import cpu_count
import copy

from multiprocessing import Pool

def exec(args):
    path, path_df = args
    boxes_list = []
    confs_list = []
    labels_list = []
    for _, model_df in path_df.groupby('model_n'):
        boxes_list.append(model_df[box_cols].values/max_value)
        confs_list.append(model_df['conf'].values.tolist())
        labels_list.append(model_df['class_id'].values.tolist())
    boxes, confs, labels = weighted_boxes_fusion(boxes_list, confs_list, labels_list, weights=[1]*len(boxes_list), iou_thr=iou_thr, skip_box_thr=skip_box_thr)
    boxes *= max_value
    results = []
    for idx, box in enumerate(boxes):
        results.append({
            "path": path,
            "class_id": int(labels[idx]),
            'conf':confs[idx],
            "x_min": box[0],
            "y_min": box[1],
            "x_max": box[2],
            "y_max": box[3],
        })
    return results

result_oof = copy.deepcopy(df_5models[0])
yolo_pred_df = pd.concat(df_5models)
weights = [1]* len(df_5models)
iou_thr = 0.4
min_conf = yolo_pred_df.conf.min()
skip_box_thr = 0.0001
results = []
max_value = 12800

class_id_name_map = {}
tmp = result_oof.drop_duplicates('class_name')
for class_id, class_name in zip(tmp.class_id.values, tmp.class_name.values):
    class_id_name_map[class_id] = class_name

wbf_result_maps_list = []
df_list = list(yolo_pred_df.groupby('path'))
p = Pool(processes=cpu_count())
with tqdm(total=len(df_list)) as pbar:
    for wbf_result_maps in p.imap(exec, df_list):
        wbf_result_maps_list += wbf_result_maps
        pbar.update(1)
p.close()

results = pd.DataFrame(wbf_result_maps_list)
for col in ['class_name', 'class_id', 'conf', 'x_min', 'y_min', 'x_max', 'y_max']:
    if col in list(result_oof):
        del result_oof[col]
results = results.merge(result_oof.drop_duplicates('path'), on='path')
results['class_name'] = results['class_id'].map(class_id_name_map)
del results['model_n']

dfs = []
for i, idf in results[['path', 'conf','class_id' ,'x_min','y_min','x_max','y_max']].groupby('path'):
    dfs.append(idf[idf.conf==idf.conf.max()].iloc[:1])
results = pd.concat(dfs)

results.to_csv(f'yolo_results_axial_left.csv', index=False)
results.head()

if plot:
    for path, pdf in results[results.path.isin(results.path.unique()[:5])].groupby('path'):
        pdf = pdf[pdf.conf==pdf.conf.max()].iloc[:1]
        im = cv2.imread(path)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        for class_id, box in zip(pdf.class_id.values, pdf[box_cols].values):
            cv2.rectangle(
                im,
                pt1=(int(box[0]), int(box[1])),
                pt2=(int(box[2]), int(box[3])),
                color=(255,255,255),
                thickness=3
            )
        plt.imshow(im[:,:,0], 'gray')
        plt.show()

# In[ ]:


box_cols = ['x_min', 'y_min', 'x_max','y_max']
yolo_for_config_dir = '/kaggle/input/rsna-2024-axial-models-v1/rsna-axial-all-images-right-yolox-x'

yolo_for_config = 'rsna_axial_all_images_right_yolox_x'

import sys
sys.path.append('/kaggle/input/yolox20230421/YOLOX')

from yolox.utils import postprocess
from yolox.data.data_augment import ValTransform


class MyDataset(Dataset):
    def __init__(self, df):
        self.paths = df.path.values
        self.preproc = ValTransform(legacy = False)
        self.size = 512

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        path = self.paths[idx]
        img = cv2.imread(path)
        ratio = min(self.size / img.shape[0], self.size / img.shape[1])

        img, _ = self.preproc(img, None, (self.size, self.size))
        img = torch.from_numpy(img).float()
        img = img.float()

        return img, path, ratio

from yolox.exp import Exp as MyExp

class ExpX(MyExp):
    def __init__(self):
        super(ExpX, self).__init__()
        self.depth = 1.33
        self.width = 1.25
        self.exp_name = ''
        self.data_dir = ""

        ### need change ###
        self.max_epoch = 10
        self.output_dir = "."
        self.input_size = (512, 512)
        self.test_size = (512, 512)
        self.no_aug_epochs = 10 # 15
        self.warmup_epochs = 5 # 5
        self.num_classes = 1
        ### need change ###

        ### fyi ###
        self.data_num_workers = 16
        self.eval_interval = 1
        self.seed = 42
        self.print_interval = 100000
        self.eval_interval = 1
        self.save_history_ckpt = False
        self.mosaic_prob = 1.0
        self.mixup_prob = 1.0
        self.hsv_prob = 1.0
        self.flip_prob = 0.5
        self.degrees = 10.0
        self.translate = 0.1
        self.mosaic_scale = (0.1, 2)
        self.enable_mixup = True
        self.mixup_scale = (0.5, 1.5)
        self.shear = 2.0
        self.min_lr_ratio = 0.05
        self.basic_lr_per_img = 0.00015625
        self.scheduler = 'yoloxwarmcos'
        self.ema = True
        self.weight_decay = 0.0005
        self.momentum = 0.9
        self.test_conf = 0.01
        self.nmsthre = 0.65
        self.class_id_name_map = {0: 'right'}

class ExpL(MyExp):
    def __init__(self):
        super(ExpL, self).__init__()
        self.depth = 1.0
        self.width = 1.0
        self.exp_name = ''
        self.data_dir = ""

        ### need change ###
        self.max_epoch = 10
        self.output_dir = "."
        self.input_size = (512, 512)
        self.test_size = (512, 512)
        self.no_aug_epochs = 10 # 15
        self.warmup_epochs = 5 # 5
        self.num_classes = 1
        ### need change ###

        ### fyi ###
        self.data_num_workers = 16
        self.eval_interval = 1
        self.seed = 42
        self.print_interval = 100000
        self.eval_interval = 1
        self.save_history_ckpt = False
        self.mosaic_prob = 1.0
        self.mixup_prob = 1.0
        self.hsv_prob = 1.0
        self.flip_prob = 0.5
        self.degrees = 10.0
        self.translate = 0.1
        self.mosaic_scale = (0.1, 2)
        self.enable_mixup = True
        self.mixup_scale = (0.5, 1.5)
        self.shear = 2.0
        self.min_lr_ratio = 0.05
        self.basic_lr_per_img = 0.00015625
        self.scheduler = 'yoloxwarmcos'
        self.ema = True
        self.weight_decay = 0.0005
        self.momentum = 0.9
        self.test_conf = 0.01
        self.nmsthre = 0.65
        self.class_id_name_map = {0: 'right'}

exp_x = ExpX()

# set inference parameters
confthre = 0.03
nmsthre = 0.45

# get YOLOX model
models = []
for fold in range(1):
    model = exp_x.get_model()
    model.to(DEVICE)
    model.eval()
    model.head.training=False
    model.training=False
    ckpt_file = "/kaggle/input/notebookfa5fb155d5/rsna-axial-all-images-right-yolox-x/0_best_ckpt.ckpt"
    # print(ckpt_file)
    ckpt = torch.load(ckpt_file, map_location="cpu")
    model.load_state_dict(ckpt["model"])
    models.append(model)

ds = MyDataset(axial_all_level_df)
loader = DataLoader(ds, batch_size=16, shuffle=False, drop_last=False, num_workers=4)

all_preds_list = [[]]
all_ratios_list = [[]]
all_paths_list = [[]]

# print('inf start...')
with torch.no_grad():
    for loader_n, input in tqdm(enumerate(loader)):
        # if loader_n % 100 == 0:
        #     print(loader_n)
        images, paths, ratios = input
        images = images.to(DEVICE)
        for model_n, model in enumerate(models):
            outputs = model(images)
            outputs = postprocess(
                        outputs, exp_x.num_classes, confthre,
                        nmsthre, class_agnostic=True
                    )
            all_preds_list[model_n] += outputs
            all_ratios_list[model_n] += list(ratios)
            all_paths_list[model_n] += list(paths)

df_5models = []
for model_n, (all_preds, all_paths, all_ratios) in enumerate(zip(all_preds_list, all_paths_list, all_ratios_list)):
    dfs = []
    all_boxes = []
    all_class_ids = []
    all_scores = []
    for n, (predictions, path, ratio)  in enumerate(zip(all_preds, all_paths, all_ratios)):
        if predictions is None:
            continue
        predictions = predictions.cpu().numpy()

        bboxes = predictions[:, 0:4]

        bboxes /= ratio
        bboxes = bboxes.tolist()
        bbclasses = predictions[:, 6]
        scores = predictions[:, 4] * predictions[:, 5]
        path_df = axial_all_level_df[axial_all_level_df.path==path].iloc[:1]
        for box, score, class_id in zip(bboxes, scores, bbclasses):
            all_boxes.append(box)
            all_scores.append(score)
            all_class_ids.append(class_id)
            dfs.append(path_df)
    tmp = pd.concat(dfs)
    tmp['class_id'] = all_class_ids
    tmp['class_id'] = tmp['class_id'].astype(int)
    tmp['class_name'] = tmp['class_id'].map(exp_x.class_id_name_map)
    tmp['conf'] = all_scores
    tmp[box_cols] = all_boxes
    tmp[box_cols] = np.round(tmp[box_cols]).astype(int)
    tmp['model_n'] = model_n
    df_5models.append(tmp)




from ensemble_boxes import *
from multiprocessing import cpu_count
import copy

from multiprocessing import Pool

def exec(args):
    path, path_df = args
    boxes_list = []
    confs_list = []
    labels_list = []
    for _, model_df in path_df.groupby('model_n'):
        boxes_list.append(model_df[box_cols].values/max_value)
        confs_list.append(model_df['conf'].values.tolist())
        labels_list.append(model_df['class_id'].values.tolist())
    boxes, confs, labels = weighted_boxes_fusion(boxes_list, confs_list, labels_list, weights=[1]*len(boxes_list), iou_thr=iou_thr, skip_box_thr=skip_box_thr)
    boxes *= max_value
    results = []
    for idx, box in enumerate(boxes):
        results.append({
            "path": path,
            "class_id": int(labels[idx]),
            'conf':confs[idx],
            "x_min": box[0],
            "y_min": box[1],
            "x_max": box[2],
            "y_max": box[3],
        })
    return results

result_oof = copy.deepcopy(df_5models[0])
yolo_pred_df = pd.concat(df_5models)
weights = [1]* len(df_5models)
iou_thr = 0.4
min_conf = yolo_pred_df.conf.min()
skip_box_thr = 0.0001
results = []
max_value = 12800

class_id_name_map = {}
tmp = result_oof.drop_duplicates('class_name')
for class_id, class_name in zip(tmp.class_id.values, tmp.class_name.values):
    class_id_name_map[class_id] = class_name

wbf_result_maps_list = []
df_list = list(yolo_pred_df.groupby('path'))
p = Pool(processes=cpu_count())
with tqdm(total=len(df_list)) as pbar:
    for wbf_result_maps in p.imap(exec, df_list):
        wbf_result_maps_list += wbf_result_maps
        pbar.update(1)
p.close()

results = pd.DataFrame(wbf_result_maps_list)
for col in ['class_name', 'class_id', 'conf', 'x_min', 'y_min', 'x_max', 'y_max']:
    if col in list(result_oof):
        del result_oof[col]
results = results.merge(result_oof.drop_duplicates('path'), on='path')
results['class_name'] = results['class_id'].map(class_id_name_map)
del results['model_n']

dfs = []
for i, idf in results[['path', 'conf','class_id' ,'x_min','y_min','x_max','y_max']].groupby('path'):
    dfs.append(idf[idf.conf==idf.conf.max()].iloc[:1])
results = pd.concat(dfs)    

results.to_csv(f'yolo_results_axial_right.csv', index=False)
results.head()
if plot:

    for path, pdf in results[results.path.isin(results.path.unique()[:5])].groupby('path'):
        pdf = pdf[pdf.conf==pdf.conf.max()].iloc[:1]
        im = cv2.imread(path)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        for class_id, box in zip(pdf.class_id.values, pdf[box_cols].values):
            cv2.rectangle(
                im,
                pt1=(int(box[0]), int(box[1])),
                pt2=(int(box[2]), int(box[3])),
                color=(255,255,255),
                thickness=3
            )
        plt.imshow(im[:,:,0], 'gray')
        plt.show()


left = pd.read_csv('yolo_results_axial_left.csv')
right = pd.read_csv('yolo_results_axial_right.csv')
for c in ['x_min', 'y_min', 'x_max', 'y_max']:
    right = right.rename(columns={c: 'right_'+c})
    left = left.rename(columns={c: 'left_'+c})
axial_box_df = right.merge(left[['path']+['left_x_min', 'left_y_min', 'left_x_max', 'left_y_max']], on='path')
axial_box_df['x_min'] = axial_box_df[['right_x_min', 'left_x_min']].min(1)
axial_box_df['y_min'] = axial_box_df[['right_y_min', 'left_y_min']].min(1)
axial_box_df['x_max'] = axial_box_df[['right_x_max', 'left_x_max']].max(1)
axial_box_df['y_max'] = axial_box_df[['right_y_max', 'left_y_max']].max(1)
axial_box_df.path.nunique(), len(axial_all_level_df)
if 'x_min' not in list(axial_all_level_df):
    axial_all_level_df = axial_all_level_df.merge(axial_box_df[['x_min', 'y_min', 'x_max', 'y_max', 'path']], on='path')


from multiprocessing import Pool

def exec(p):
    im=cv2.imread(p)
    return im.shape[:2]

p = Pool(processes=4)
args = axial_all_level_df.path.values
results = p.map(exec, args)    
image_size_df = pd.DataFrame(results)
image_size_df.columns = ['image_height', 'image_width']
image_size_df['path'] = args
if 'image_height' not in list(axial_all_level_df):
    axial_all_level_df = axial_all_level_df.merge(image_size_df, on='path')
axial_all_level_df = axial_all_level_df.sort_values(['series_id', 'pred_level'])    
axial_all_level_df.to_csv('axial_with_box_df.csv', index=False)    
axial_all_level_df.head(6)

# In[ ]:


box_cols = ['x_min', 'y_min', 'x_max','y_max']
yolo_for_config_dir = '/kaggle/input/rsna-10classes-yolox-x'
yolo_for_config = 'rsna_10classes_yolox_x'

import sys
sys.path.append('/kaggle/input/yolox20230421/YOLOX')

from yolox.utils import postprocess
from yolox.data.data_augment import ValTransform

class MyDataset(Dataset):
    def __init__(self, df):
        self.paths = df.path.values
        self.preproc = ValTransform(legacy = False)
        self.size = 512

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        path = self.paths[idx]
        img = cv2.imread(path)
        ratio = min(self.size / img.shape[0], self.size / img.shape[1])

        img, _ = self.preproc(img, None, (self.size, self.size))
        img = torch.from_numpy(img).float()
        img = img.float()

        return img, path, ratio

from yolox.exp import Exp as MyExp

class Exp(MyExp):
    def __init__(self):
        super(Exp, self).__init__()
        self.depth = 1.33
        self.width = 1.25
        self.exp_name = ''
        self.data_dir = ""

        ### need change ###
        self.max_epoch = 10
        self.output_dir = "."
        self.input_size = (512, 512)
        self.test_size = (512, 512)
        self.no_aug_epochs = 10 # 15
        self.warmup_epochs = 5 # 5
        self.num_classes = 10
        ### need change ###

        ### fyi ###
        self.data_num_workers = 16
        self.eval_interval = 1
        self.seed = 42
        self.print_interval = 100
        self.eval_interval = 1
        self.save_history_ckpt = False
        self.mosaic_prob = 1.0
        self.mixup_prob = 1.0
        self.hsv_prob = 1.0
        self.flip_prob = 0.5
        self.degrees = 10.0
        self.translate = 0.1
        self.mosaic_scale = (0.1, 2)
        self.enable_mixup = True
        self.mixup_scale = (0.5, 1.5)
        self.shear = 2.0
        self.min_lr_ratio = 0.05
        self.basic_lr_per_img = 0.00015625
        self.scheduler = 'yoloxwarmcos'
        self.ema = True
        self.weight_decay = 0.0005
        self.momentum = 0.9
        self.test_conf = 0.01
        self.nmsthre = 0.65
        self.class_id_name_map = {
             0: 'L1/L2_L',
             1: 'L1/L2_R',
             2: 'L2/L3_L',
             3: 'L2/L3_R',
             4: 'L3/L4_L',
             5: 'L3/L4_R',
             6: 'L4/L5_L',
             7: 'L4/L5_R',
             8: 'L5/S1_L',
             9: 'L5/S1_R'
        }

exp = Exp()

# set inference parameters
confthre = 0.03
nmsthre = 0.45

# get YOLOX model
models = []
for fold in range(5):
    model = exp.get_model()
    model.cuda()
    model.eval()
    model.head.training=False
    model.training=False
    if debug:
        ckpt_file = f"/kaggle/input/notebookfa5fb155d5/rsna-10classes-yolox-x/{debug_fold}_best_ckpt.ckpt"
    else:
        ckpt_file = f"/kaggle/input/notebookfa5fb155d5/rsna-10classes-yolox-x/{fold}_best_ckpt.ckpt"
    # print(ckpt_file)
    ckpt = torch.load(ckpt_file, map_location="cpu")
    model.load_state_dict(ckpt["model"])
    models.append(model)
ds = MyDataset(spinal_sagittal)
loader = DataLoader(ds, batch_size=16, shuffle=False, drop_last=False, num_workers=4)

all_preds_list = [[], [], [], [], []]
all_ratios_list = [[], [], [], [], []]
all_paths_list = [[], [], [], [], []]

# print('inf start...')
with torch.no_grad():
    for loader_n, input in tqdm(enumerate(loader)):
        # if loader_n % 100 == 0:
        #     print(loader_n)
        images, paths, ratios = input
        images = images.cuda()
        for model_n, model in enumerate(models):
            outputs = model(images)
            outputs = postprocess(
                        outputs, exp.num_classes, confthre,
                        nmsthre, class_agnostic=True
                    )
            all_preds_list[model_n] += outputs
            all_ratios_list[model_n] += list(ratios)
            all_paths_list[model_n] += list(paths)

df_5models = []
for model_n, (all_preds, all_paths, all_ratios) in enumerate(zip(all_preds_list, all_paths_list, all_ratios_list)):
    dfs = []
    all_boxes = []
    all_class_ids = []
    all_scores = []
    for n, (predictions, path, ratio)  in enumerate(zip(all_preds, all_paths, all_ratios)):
        if predictions is None:
            continue
        predictions = predictions.cpu().numpy()

        bboxes = predictions[:, 0:4]

        bboxes /= ratio
        bboxes = bboxes.tolist()
        bbclasses = predictions[:, 6]
        scores = predictions[:, 4] * predictions[:, 5]
        path_df = sagittal_df[sagittal_df.path==path]
        for box, score, class_id in zip(bboxes, scores, bbclasses):
            all_boxes.append(box)
            all_scores.append(score)
            all_class_ids.append(class_id)
            dfs.append(path_df)
    tmp = pd.concat(dfs)
    tmp['class_id'] = all_class_ids
    tmp['class_id'] = tmp['class_id'].astype(int)
    tmp['class_name'] = tmp['class_id'].map(exp.class_id_name_map)
    tmp['conf'] = all_scores
    tmp[box_cols] = all_boxes
    tmp[box_cols] = np.round(tmp[box_cols]).astype(int)
    tmp['model_n'] = model_n
    df_5models.append(tmp)

from ensemble_boxes import *
from multiprocessing import cpu_count
import copy

from multiprocessing import Pool

def exec(args):
    path, path_df = args
    boxes_list = []
    confs_list = []
    labels_list = []
    for _, model_df in path_df.groupby('model_n'):
        boxes_list.append(model_df[box_cols].values/max_value)
        confs_list.append(model_df['conf'].values.tolist())
        labels_list.append(model_df['class_id'].values.tolist())
    boxes, confs, labels = weighted_boxes_fusion(boxes_list, confs_list, labels_list, weights=[1]*len(boxes_list), iou_thr=iou_thr, skip_box_thr=skip_box_thr)
    boxes *= max_value
    results = []
    for idx, box in enumerate(boxes):
        results.append({
            "path": path,
            "class_id": int(labels[idx]),
            'conf':confs[idx],
            "x_min": box[0],
            "y_min": box[1],
            "x_max": box[2],
            "y_max": box[3],
        })
    return results

result_oof = copy.deepcopy(df_5models[0])
yolo_pred_df = pd.concat(df_5models)
weights = [1]* len(df_5models)
iou_thr = 0.4
min_conf = yolo_pred_df.conf.min()
skip_box_thr = 0.0001
results = []
max_value = 12800

class_id_name_map = {}
tmp = result_oof.drop_duplicates('class_name')
for class_id, class_name in zip(tmp.class_id.values, tmp.class_name.values):
    class_id_name_map[class_id] = class_name

wbf_result_maps_list = []
df_list = list(yolo_pred_df.groupby('path'))
p = Pool(processes=cpu_count())
with tqdm(total=len(df_list)) as pbar:
    for wbf_result_maps in p.imap(exec, df_list):
        wbf_result_maps_list += wbf_result_maps
        pbar.update(1)
p.close()

results = pd.DataFrame(wbf_result_maps_list)
for col in ['class_name', 'class_id', 'conf', 'x_min', 'y_min', 'x_max', 'y_max']:
    if col in list(result_oof):
        del result_oof[col]
results = results.merge(result_oof.drop_duplicates('path'), on='path')
results['class_name'] = results['class_id'].map(class_id_name_map)
del results['model_n']

dfs = []
for i, idf in results.groupby(['path', 'class_id']):
    dfs.append(idf[idf.conf==idf.conf.max()].iloc[:1])
results = pd.concat(dfs)    


results.to_csv(f'yolo_results_sagittal.csv', index=False)
results.head()
if plot:

    for path, pdf in results[results.path.isin(results.path.unique()[:5])].groupby('path'):
        im = cv2.imread(path)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        for class_id, box in zip(pdf.class_id.values, pdf[box_cols].values):
            cv2.rectangle(
                im,
                pt1=(int(box[0]), int(box[1])),
                pt2=(int(box[2]), int(box[3])),
                color=(255,255,255),
                thickness=3
            )
        plt.imshow(im[:,:,0], 'gray')
        plt.show()

del models
torch.cuda.empty_cache()


spinal_sagittal = pd.read_csv('spinal_sagittal_df.csv')
l = len(spinal_sagittal)
yolo_results_sagittal = pd.read_csv('yolo_results_sagittal.csv')[['path', 'class_id', 'class_name', 'conf','x_min','y_min','x_max','y_max']]
yolo_results_sagittal['study_id'] = yolo_results_sagittal.path.apply(lambda x: int(x.split('/')[-1].split('___')[0]))
del yolo_results_sagittal['path']

sagittal_box_df = spinal_sagittal.merge(yolo_results_sagittal, on='study_id')
sagittal_box_df['level'] = sagittal_box_df.class_name.apply(lambda x: x.split('_')[0])
sagittal_box_df['lr'] = sagittal_box_df.class_name.apply(lambda x: x.split('_')[1])
sagittal_box_df = sagittal_box_df[['study_id', 'path', 'level', 'lr']+box_cols]
sagittal_box_df.to_csv('sagittal_box_df.csv', index=False)

sagittal_df = pd.read_csv('sagittal_df.csv')                                                        


# # classification for axial

# In[ ]:


class axial_base(base):
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv('axial_with_box_df.csv')
        cols = []
        label_features = [
            'spinal_canal_stenosis',
            # 'left_neural_foraminal_narrowing',
            # 'right_neural_foraminal_narrowing',
            # 'left_subarticular_stenosis',
            # 'right_subarticular_stenosis',
        ]
        for col in label_features:
            cols.append(f'{col}_normal')
            cols.append(f'{col}_moderate')
            cols.append(f'{col}_severe')
        self.label_features = cols
        self.model = timm.create_model(self.model_name, pretrained=False, num_classes=len(self.label_features))
        d = '/kaggle/input/rsna-2024-axial-models-v1/rsna-axial-spinal-dis3-crop-x05-y6'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.transforms = A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(),
            ToTensorV2(),
        ])
        self.batch_size = 16

class rsna_axial_spinal_ss_dis3(axial_base):
    def __init__(self):
        super().__init__()
        cols = []
        label_features = [
            'spinal_canal_stenosis',
            # 'left_neural_foraminal_narrowing',
            # 'right_neural_foraminal_narrowing',
            'left_subarticular_stenosis',
            'right_subarticular_stenosis',
        ]
        for col in label_features:
            cols.append(f'{col}_normal')
            cols.append(f'{col}_moderate')
            cols.append(f'{col}_severe')
        self.label_features = cols
        self.model = timm.create_model(self.model_name, pretrained=False, num_classes=len(self.label_features))
        d = '/kaggle/input/rsna-2024-reduce-noise-models/axial-spinal-ss-reduce-noise-08'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'
            
class rsna_axial_spinal_dis3_crop_x05_y6(axial_base):
    def __init__(self):
        super().__init__()
        cols = []
        label_features = [
            'spinal_canal_stenosis',
            # 'left_neural_foraminal_narrowing',
            # 'right_neural_foraminal_narrowing',
#             'left_subarticular_stenosis',
#             'right_subarticular_stenosis',
        ]
        for col in label_features:
            cols.append(f'{col}_normal')
            cols.append(f'{col}_moderate')
            cols.append(f'{col}_severe')
        self.label_features = cols
        self.model = timm.create_model(self.model_name, pretrained=False, num_classes=len(self.label_features))
        d = '/kaggle/input/rsna-2024-reduce-noise-models/axial-spinal-dis3-crop-x05-y6-reduce-noise-08'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.box_crop = True
        self.box_crop_x_ratio = 0.5
        self.box_crop_y_ratio = 6
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'
            
class rsna_axial_spinal_dis3_crop_x1_y2(axial_base):
    def __init__(self):
        super().__init__()
        cols = []
        label_features = [
            'spinal_canal_stenosis',
            # 'left_neural_foraminal_narrowing',
            # 'right_neural_foraminal_narrowing',
#             'left_subarticular_stenosis',
#             'right_subarticular_stenosis',
        ]
        for col in label_features:
            cols.append(f'{col}_normal')
            cols.append(f'{col}_moderate')
            cols.append(f'{col}_severe')
        self.label_features = cols
        self.model = timm.create_model(self.model_name, pretrained=False, num_classes=len(self.label_features))
        d = '/kaggle/input/rsna-2024-reduce-noise-models/axial-spinal-dis3-crop-x1-y2-reduce-noise-08'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.box_crop = True
        self.box_crop_x_ratio = 1
        self.box_crop_y_ratio = 2
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'


class rsna_axial_ss_nfn_x2_y2_center_pad0(axial_base):
    def __init__(self):
        super().__init__()
        self.box_crop = True
        self.box_crop_x_ratio = 0
        image_width_ratio = 2
        self.box_crop_y_ratio = 2
        center_pad_ratio = 0

        df_path = 'axial_with_box_df.csv'

        df_left = pd.read_csv(df_path)
        df_left['x_min'] = (df_left.x_max + df_left.x_min)/2
        del df_left['x_max']
        df_left['left_right'] = 'left'
        if center_pad_ratio != 0:
            df_left['x_min'] = df_left['x_min'] - df_left['image_width']/center_pad_ratio
        df_left['x_max'] = df_left['x_min'] + df_left['image_width']/image_width_ratio

        df_right = pd.read_csv(df_path)
        df_right['x_max'] = (df_right.x_max + df_right.x_min)/2
        del df_right['x_min']
        df_right['left_right'] = 'right'
        df_right['x_min'] = df_right['x_max'] - df_right['image_width']/image_width_ratio
        if center_pad_ratio != 0:
            df_right['x_max'] = df_right['x_max'] + df_right['image_width']/center_pad_ratio

        self.df = pd.concat([df_left, df_right])

        # self.df = self.df[(self.df.dis < 3) | (self.df.dis.isnull())]

        cols = []
        label_features = [
            'neural_foraminal_narrowing',
            'subarticular_stenosis',
        ]
        for col in label_features:
            cols.append(f'{col}_normal')
            cols.append(f'{col}_moderate')
            cols.append(f'{col}_severe')

        self.label_features = cols
        self.image_size = 384
        self.drop_rate = 0.0
        self.drop_path_rate = 0.0
        self.model = timm.create_model(self.model_name, pretrained=False, num_classes=len(self.label_features),
            drop_rate=self.drop_rate, drop_path_rate=self.drop_path_rate)
        n = 'axial_ss_nfn_x2_y2_pad0_reduce_noise'
        d = f'/kaggle/input/rsna-2024-reduce-noise-models-v2/{n.replace("_", "-")}'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'

class rsna_axial_ss_nfn_x2_y6_center_pad0(axial_base):
    def __init__(self):
        super().__init__()
        self.box_crop = True
        self.box_crop_x_ratio = 0
        image_width_ratio = 2
        self.box_crop_y_ratio = 6
        center_pad_ratio = 0

        df_path = 'axial_with_box_df.csv'

        df_left = pd.read_csv(df_path)
        df_left['x_min'] = (df_left.x_max + df_left.x_min)/2
        del df_left['x_max']
        df_left['left_right'] = 'left'
        if center_pad_ratio != 0:
            df_left['x_min'] = df_left['x_min'] - df_left['image_width']/center_pad_ratio
        df_left['x_max'] = df_left['x_min'] + df_left['image_width']/image_width_ratio

        df_right = pd.read_csv(df_path)
        df_right['x_max'] = (df_right.x_max + df_right.x_min)/2
        del df_right['x_min']
        df_right['left_right'] = 'right'
        df_right['x_min'] = df_right['x_max'] - df_right['image_width']/image_width_ratio
        if center_pad_ratio != 0:
            df_right['x_max'] = df_right['x_max'] + df_right['image_width']/center_pad_ratio

        self.df = pd.concat([df_left, df_right])

        # self.df = self.df[(self.df.dis < 3) | (self.df.dis.isnull())]

        cols = []
        label_features = [
            'neural_foraminal_narrowing',
            'subarticular_stenosis',
        ]
        for col in label_features:
            cols.append(f'{col}_normal')
            cols.append(f'{col}_moderate')
            cols.append(f'{col}_severe')

        self.label_features = cols
        self.image_size = 384
        self.drop_rate = 0.0
        self.drop_path_rate = 0.0
        self.model = timm.create_model(self.model_name, pretrained=False, num_classes=len(self.label_features),
            drop_rate=self.drop_rate, drop_path_rate=self.drop_path_rate)
        n = 'axial_ss_nfn_x2_y6_pad0_reduce_noise'
        d = f'/kaggle/input/rsna-2024-reduce-noise-models-v2/{n.replace("_", "-")}'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'
class rsna_axial_ss_nfn_x2_y8_center_pad10(axial_base):
    def __init__(self):
        super().__init__()
        self.box_crop = True
        self.box_crop_x_ratio = 0
        image_width_ratio = 2
        self.box_crop_y_ratio = 8
        center_pad_ratio = 10

        df_path = 'axial_with_box_df.csv'

        df_left = pd.read_csv(df_path)
        df_left['x_min'] = (df_left.x_max + df_left.x_min)/2
        del df_left['x_max']
        df_left['left_right'] = 'left'
        if center_pad_ratio != 0:
            df_left['x_min'] = df_left['x_min'] - df_left['image_width']/center_pad_ratio
        df_left['x_max'] = df_left['x_min'] + df_left['image_width']/image_width_ratio

        df_right = pd.read_csv(df_path)
        df_right['x_max'] = (df_right.x_max + df_right.x_min)/2
        del df_right['x_min']
        df_right['left_right'] = 'right'
        df_right['x_min'] = df_right['x_max'] - df_right['image_width']/image_width_ratio
        if center_pad_ratio != 0:
            df_right['x_max'] = df_right['x_max'] + df_right['image_width']/center_pad_ratio

        self.df = pd.concat([df_left, df_right])

        # self.df = self.df[(self.df.dis < 3) | (self.df.dis.isnull())]

        cols = []
        label_features = [
            'neural_foraminal_narrowing',
            'subarticular_stenosis',
        ]
        for col in label_features:
            cols.append(f'{col}_normal')
            cols.append(f'{col}_moderate')
            cols.append(f'{col}_severe')

        self.label_features = cols
        self.image_size = 384
        self.drop_rate = 0.0
        self.drop_path_rate = 0.0
        self.model = timm.create_model(self.model_name, pretrained=False, num_classes=len(self.label_features),
            drop_rate=self.drop_rate, drop_path_rate=self.drop_path_rate)
        n = 'axial_ss_nfn_x2_y8_pad10_reduce_noise'
        d = f'/kaggle/input/rsna-2024-reduce-noise-models-v2/{n.replace("_", "-")}'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'


# In[ ]:


import copy
config_names = [
    'rsna_axial_ss_nfn_x2_y2_center_pad0',
    'rsna_axial_ss_nfn_x2_y6_center_pad0',
    'rsna_axial_ss_nfn_x2_y8_center_pad10',

    'rsna_axial_spinal_dis3_crop_x05_y6',
    'rsna_axial_spinal_dis3_crop_x1_y2',
]
for config_name in config_names:
    cfg = eval(config_name)()
    models = []
    for model_path in cfg.model_paths:
        state_dict = torch.load(model_path, map_location=torch.device('cpu'))
        model = copy.deepcopy(cfg.model)
        model.load_state_dict(state_dict)
        model.to(DEVICE)
        model.eval()
        models.append(model)


    ds = RSNA2024DatasetV1(cfg)
    loader = DataLoader(ds, batch_size=cfg.batch_size, shuffle=False, drop_last=False, num_workers=4)
    preds = []
    for images in tqdm(loader, smoothing=0):
        images = images.to(DEVICE)
        batch_preds = []
        for model in models:
            batch_preds.append(model(images).detach().cpu().numpy())

        if cfg.tta:
            imsize = images.size()
            images = torch.flip(images, (3,))
            assert imsize == images.size()
            for model in models:
                batch_preds.append(model(images).detach().cpu().numpy())

        preds += np.mean(batch_preds, axis=0).tolist()
    pred_cols = [f'pred_{c}' for c in cfg.label_features]
    cfg.df[pred_cols] = np.array(preds)
    cfg.df.to_csv(f'{config_name}.csv', index=False)


# # sagittal classification

# In[ ]:


# preprocess for classification

rolling = 5
range_n  = 2

saigittal_box_df = pd.read_csv('sagittal_box_df.csv')
sagittal_df = pd.read_csv('sagittal_df.csv')
sagittal_df.path = '/kaggle/temp/sagittal_all_images/' + sagittal_df.study_id.astype(str) + '___' + sagittal_df.instance_number.astype(str) + '.png'

dfs = []
for id, idf in sagittal_df.groupby('series_id'):
    idf = idf.sort_values(['x_pos', 'instance_number'])
    idf = idf.drop_duplicates('x_pos')
    idf[f'pred_spinal_rolling'] = idf[f'pred_spinal'].rolling(rolling, center=True).mean()    

    paths = []
    for col in ['pred_spinal_rolling']:
        n = idf[idf[col]==idf[col].max()].instance_number.values[0]
    
        ldf = idf[(idf.instance_number >= n-range_n) & (idf.instance_number <= n+range_n)]
        l_paths = ['nan'] * (1+range_n*2)
        for path_n, path in enumerate(ldf.path):
            l_paths[path_n] = path
        paths += l_paths
    ldf = ldf.iloc[:1]
    ldf['paths'] = ','.join(paths)
    dfs.append(ldf)
spinal_df = pd.concat(dfs)
spinal_df = spinal_df.drop_duplicates('study_id')
del spinal_df['path']
spinal_df = spinal_df.merge(saigittal_box_df, on=['study_id'])
dfs = []
for i, idf in spinal_df.groupby(['study_id', 'level']):
    l = idf[idf.lr == 'L']
    r = idf[idf.lr == 'R']
    if (len(l) == 0) | (len(r) == 0):
        continue
    idf['l_x'] = (l.x_max.values[0] + l.x_min.values[0])/2
    idf['l_y'] = (l.y_max.values[0] + l.y_min.values[0])/2
    idf['r_x'] = (r.x_max.values[0] + r.x_min.values[0])/2
    idf['r_y'] = (r.y_max.values[0] + r.y_min.values[0])/2
    idf = idf.iloc[:1]
    dfs.append(idf)
spinal_df = pd.concat(dfs)

p = f'sagittal_spinal_range{range_n}_rolling{rolling}_v2.csv'
spinal_df.to_csv(p, index=False)
# print(p)

rolling = 5
range_n  = 2

saigittal_box_df = pd.read_csv('sagittal_box_df.csv')
sagittal_df = pd.read_csv('sagittal_df.csv')
sagittal_df = sagittal_df[sagittal_df.series_id.isin(t2_ids)]
dfs = []
for id, idf in sagittal_df.groupby('series_id'):
    idf = idf.sort_values(['x_pos', 'instance_number'])
    idf = idf.drop_duplicates('x_pos')
    idf[f'pred_spinal_rolling'] = idf[f'pred_spinal'].rolling(rolling, center=True).mean()    

    paths = []
    for col in ['pred_spinal_rolling']:
        n = idf[idf[col]==idf[col].max()].instance_number.values[0]
    
        ldf = idf[(idf.instance_number >= n-range_n) & (idf.instance_number <= n+range_n)]
        l_paths = ['nan'] * (1+range_n*2)
        for path_n, path in enumerate(ldf.path):
            l_paths[path_n] = path
        paths += l_paths
    ldf = ldf.iloc[:1]
    ldf['paths'] = ','.join(paths)
    dfs.append(ldf)
spinal_df = pd.concat(dfs)
spinal_df = spinal_df.drop_duplicates('study_id')
del spinal_df['path']
spinal_df = spinal_df.merge(saigittal_box_df, on=['study_id'])
dfs = []
for i, idf in spinal_df.groupby(['study_id', 'level']):
    l = idf[idf.lr == 'L']
    r = idf[idf.lr == 'R']
    if (len(l) == 0) | (len(r) == 0):
        continue
    idf['l_x'] = (l.x_max.values[0] + l.x_min.values[0])/2
    idf['l_y'] = (l.y_max.values[0] + l.y_min.values[0])/2
    idf['r_x'] = (r.x_max.values[0] + r.x_min.values[0])/2
    idf['r_y'] = (r.y_max.values[0] + r.y_min.values[0])/2
    idf = idf.iloc[:1]
    dfs.append(idf)
spinal_df = pd.concat(dfs)

p = f'sagittal_spinal_range{range_n}_rolling{rolling}_t2.csv'
spinal_df.to_csv(p, index=False)

rolling = 5
range_n  = 2

for left_right in ['left', 'right']:
    col = f'pred_{left_right}_neural_rolling'
    saigittal_box_df = pd.read_csv('sagittal_box_df.csv')
    sagittal_df = pd.read_csv('sagittal_df.csv')
    sagittal_df.path = '/kaggle/temp/sagittal_all_images/' + sagittal_df.study_id.astype(str) + '___' + sagittal_df.instance_number.astype(str) + '.png'

    dfs = []
    for id, idf in sagittal_df.groupby('series_id'):
        idf = idf.sort_values(['x_pos', 'instance_number'])
        idf = idf.drop_duplicates('x_pos')
        idf[col] = idf[f'pred_{left_right}_neural'].rolling(rolling, center=True).mean()

        n = idf[idf[col]==idf[col].max()].instance_number.values[0]
    
        ldf = idf[(idf.instance_number >= n-range_n) & (idf.instance_number <= n+range_n)]
        l_paths = ['nan'] * (1+range_n*2)
        for path_n, path in enumerate(ldf.path):
            l_paths[path_n] = path
        ldf = ldf.iloc[:1]
        ldf['paths'] = ','.join(l_paths)
        dfs.append(ldf)
    nfn_df = pd.concat(dfs)
    nfn_df = nfn_df.drop_duplicates('study_id')
    del nfn_df['path']
    nfn_df = nfn_df.merge(saigittal_box_df, on=['study_id'])
    dfs = []
    for i, idf in nfn_df.groupby(['study_id', 'level']):
        l = idf[idf.lr == 'L']
        r = idf[idf.lr == 'R']
        if (len(l) == 0) | (len(r) == 0):
            continue
        idf['l_x'] = (l.x_max.values[0] + l.x_min.values[0])/2
        idf['l_y'] = (l.y_max.values[0] + l.y_min.values[0])/2
        idf['r_x'] = (r.x_max.values[0] + r.x_min.values[0])/2
        idf['r_y'] = (r.y_max.values[0] + r.y_min.values[0])/2
        idf = idf.iloc[:1]
        dfs.append(idf)
    nfn_df = pd.concat(dfs)

    p = f'sagittal_{left_right}_nfn_range{range_n}_rolling{rolling}.csv'
    nfn_df.to_csv(p, index=False)

rolling = 5
range_n  = 2

for left_right in ['left', 'right']:
    col = f'pred_{left_right}_neural_rolling'
    saigittal_box_df = pd.read_csv('sagittal_box_df.csv')
    sagittal_df = pd.read_csv('sagittal_df.csv')
    sagittal_df.path = '/kaggle/temp/sagittal_all_images/' + sagittal_df.study_id.astype(str) + '___' + sagittal_df.instance_number.astype(str) + '.png'

    dfs = []
    for id, idf in sagittal_df.groupby('series_id'):
        idf = idf.sort_values(['x_pos', 'instance_number'])
        idf = idf.drop_duplicates('x_pos')
        idf['pred_spinal_rolling'] = idf[f'pred_spinal'].rolling(rolling, center=True).mean()        
        idf[col] = idf[f'pred_{left_right}_neural'].rolling(rolling, center=True).mean()

        spinal_n = idf[idf['pred_spinal_rolling']==idf['pred_spinal_rolling'].max()].instance_number.values[0]
        n = idf[idf[col]==idf[col].max()].instance_number.values[0]
        n = (spinal_n + n)//2
    
        ldf = idf[(idf.instance_number >= n-range_n) & (idf.instance_number <= n+range_n)]
        l_paths = ['nan'] * (1+range_n*2)
        for path_n, path in enumerate(ldf.path):
            l_paths[path_n] = path
        ldf = ldf.iloc[:1]
        ldf['paths'] = ','.join(l_paths)
        dfs.append(ldf)
    nfn_df = pd.concat(dfs)
    nfn_df = nfn_df.drop_duplicates('study_id')
    del nfn_df['path']
    nfn_df = nfn_df.merge(saigittal_box_df, on=['study_id'])
    dfs = []
    for i, idf in nfn_df.groupby(['study_id', 'level']):
        l = idf[idf.lr == 'L']
        r = idf[idf.lr == 'R']
        if (len(l) == 0) | (len(r) == 0):
            continue
        idf['l_x'] = (l.x_max.values[0] + l.x_min.values[0])/2
        idf['l_y'] = (l.y_max.values[0] + l.y_min.values[0])/2
        idf['r_x'] = (r.x_max.values[0] + r.x_min.values[0])/2
        idf['r_y'] = (r.y_max.values[0] + r.y_min.values[0])/2
        idf = idf.iloc[:1]
        dfs.append(idf)
    nfn_df = pd.concat(dfs)

    p = f'sagittal_{left_right}_ss_range{range_n}_rolling{rolling}.csv'
    nfn_df.to_csv(p, index=False)


# In[ ]:


import math
def crop_between_keypoints(img, keypoint1, keypoint2, ratio=0.1):
    h, w = img.shape[:2]
    x1, y1 = int(keypoint1[0]), int(keypoint1[1])
    x2, y2 = int(keypoint2[0]), int(keypoint2[1])
    
    # Calculate bounding box around the keypoints
    left = int(min(x1, x2))
    right = int(max(x1, x2))
    top = int(min(y1, y2) - (h * 0.1))
    bottom = int(max(y1, y2) + (h * 0.1))
            
    # Crop the image
    return img[top:bottom, left:right, :]

def angle_of_line(x1, y1, x2, y2):
    return math.degrees(math.atan2(-(y2-y1), x2-x1))

class RSNA2024DatasetMIL(Dataset):
    def __init__(self, cfg):
        self.transforms = cfg.transforms
        self.paths = cfg.df.path.values
        self.paths_list = cfg.df.paths.values
        self.cfg = cfg
        self.l_points = cfg.df[['l_x', 'l_y']].values
        self.r_points = cfg.df[['r_x', 'r_y']].values

    def __len__(self):
        return len(self.paths)

    def load_image(self, path, a, b, origin_size):
        if path == 'nan':
            image = np.zeros((origin_size[0], origin_size[1], 3)).astype(np.uint8)
        else:
            image = cv2.imread(path)
            image = cv2.resize(image, (origin_size[1], origin_size[0]))

        rotate_angle = angle_of_line(a[0], a[1], b[0], b[1])
        transform = A.Compose([
            A.Rotate(limit=(-rotate_angle, -rotate_angle), p=1.0),
        ], keypoint_params= A.KeypointParams(format='xy', remove_invisible=False),
        )

        t = transform(image=image, keypoints=[a, b])
        image = t["image"]
        a, b = t["keypoints"]
        if a[0]<0:
            a = (0, a[1])
        if b[0]<0:
            b = (0, b[1])
        if a[1]<0:
            a = (a[0], 0)
        if b[1]<0:
            b = (b[0], 0) 
        if self.cfg.box_crop:
            if ((hasattr(self.cfg, 'xy_center_point')) and (self.cfg.xy_center_point)):
                x = int((a[0]+b[0])/2)
                y = int((a[1]+b[1])/2)
            else:
                x = int(b[0])
                y = int(b[1])
            
            w = abs(b[0]-a[0])
            h = image.shape[0]*0.2

            crop_x = int(w * self.cfg.box_crop_x_ratio)
            crop_y = int(h * self.cfg.box_crop_y_ratio)
            x_min = max(x-crop_x, 0)
            y_min = max(y-crop_y, 0)

            image = image[y_min:y+crop_y, x_min:x+crop_x]
        else:
            image = crop_between_keypoints(image, a, b)
        return image

    def __getitem__(self, idx):
        path = self.paths[idx]
        paths = self.paths_list[idx]

        origin_size = cv2.imread(path).shape[:2]
        a = self.l_points[idx]
        b = self.r_points[idx]
        images = []
        for path in paths.split(','):
            image = self.load_image(path, a, b, origin_size)
            images.append(self.transforms(image=image.astype(np.uint8))['image'])

        images = np.stack(images, 0)
        images = torch.tensor(images).float()

        return images

class Flatten(nn.Module):
    def __init__(self, dim=1):
        super().__init__()
        self.dim = dim

    def forward(self, x):
        input_shape = x.shape
        output_shape = [input_shape[i] for i in range(self.dim)] + [-1]
        return x.view(*output_shape)

class AdaptiveConcatPool2d(nn.Module):
    def __init__(self, sz=None, flatten=False):
        super().__init__()
        sz = sz or (1, 1)
        self.ap = nn.AdaptiveAvgPool2d(sz)
        self.mp = nn.AdaptiveMaxPool2d(sz)
        self.flatten_layer = Flatten()
        self.flatten = flatten

    def forward(self, x):
        x = torch.cat([self.mp(x), self.ap(x)], 1)
        if self.flatten:
            x = self.flatten_layer(x)
        return x


def drop_fc(model):
    nc = model.head.fc.in_features
    model.head.global_pool = nn.Identity()
    model.head.norm = nn.Identity()
    model.head.flatten = nn.Identity()
    model.head.drop = nn.Identity()
    model.head.fc = nn.Identity()
    new_model = model

    return new_model, nc

class RSNA2ndModel(nn.Module):
    def __init__(
        self,
        num_classes=1,
        base_model=None,
    ):
        super().__init__()
        self.encoder, nc = drop_fc(base_model)
        self.head = nn.Sequential(
            AdaptiveConcatPool2d(),
            Flatten(),
            nn.Linear(2 * nc, num_classes),
        )
    def forward(self, x):
        bs, n, ch, w, h = x.shape
        x = x.view(bs * n, ch, w, h)
        x = self.encoder(x)
        bs2, ch2, w2, h2 = x.shape

        x = (
            x.view(-1, n, ch2, w2, h2)
            .permute(0, 2, 1, 3, 4)
            .contiguous()
            .view(bs, ch2, n * w2, h2)
        )

        x = self.head(x)
        return x


# In[ ]:


class rsna_saggital_spinal_v2(base):
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv('sagittal_spinal_range2_rolling5_v2.csv')
        self.label_features = [
            'spinal_canal_stenosis_normal',
            'spinal_canal_stenosis_moderate',
            'spinal_canal_stenosis_severe',
        ]
        self.drop_rate = 0.0
        self.drop_path_rate = 0.0        
        base_model = timm.create_model(self.model_name, pretrained=False, num_classes=1,
            drop_rate=self.drop_rate, drop_path_rate=self.drop_path_rate)
        self.model = RSNA2ndModel(
            base_model=base_model,
            num_classes=len(self.label_features)
        )
        
        d = '/kaggle/input/rsna-2024-reduce-noise-models-v2/rsna-saggital-spinal-v2'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'

        self.image_size = 128
        self.transforms = A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(),
            ToTensorV2(),
        ])
        self.box_crop = True
        self.box_crop_x_ratio = 0.5
        self.box_crop_y_ratio = 0.5
        self.xy_center_point = True
        
class rsna_saggital_mil_spinal_crop_x03_y05(rsna_saggital_spinal_v2):
    def __init__(self):
        super().__init__()        
        self.box_crop_x_ratio = 0.3
        self.box_crop_y_ratio = 0.5
        self.xy_center_point = False
        d = '/kaggle/input/rsna-2024-reduce-noise-models/saggital-spinal-x03-y05-reduce-noise'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'
        
class rsna_saggital_mil_spinal_crop_x03_y07(rsna_saggital_spinal_v2):
    def __init__(self):
        super().__init__()        
        self.box_crop_x_ratio = 0.3
        self.box_crop_y_ratio = 0.7
        self.xy_center_point = False
        d = '/kaggle/input/rsna-2024-reduce-noise-models/saggital-spinal-x03-y07-reduce-noise'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'
        
class rsna_saggital_mil_spinal_crop_x05_y15(rsna_saggital_spinal_v2):
    def __init__(self):
        super().__init__()        
        self.box_crop_x_ratio = 0.5
        self.box_crop_y_ratio = 1.5
        self.xy_center_point = False
        d = '/kaggle/input/rsna-2024-reduce-noise-models-v2/rsna-saggital-mil-spinal-crop-x05-y15'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'

class rsna_saggital_mil_spinal_crop_x03_y07_t2_v4(rsna_saggital_spinal_v2):
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv('sagittal_spinal_range2_rolling5_t2.csv')
        self.label_features = [
            'spinal_canal_stenosis_normal',
            'spinal_canal_stenosis_moderate',
            'spinal_canal_stenosis_severe',
        ]
        self.drop_rate = 0.0
        self.drop_path_rate = 0.0        
        base_model = timm.create_model(self.model_name, pretrained=False, num_classes=1,
            drop_rate=self.drop_rate, drop_path_rate=self.drop_path_rate)
        self.model = RSNA2ndModel(
            base_model=base_model,
            num_classes=len(self.label_features)
        )

        
        d = '/kaggle/input/rsna-2024-reduce-noise-models/saggital-spinal-x03-y07-t2-reduce-noise'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'

        self.box_crop = True
        self.box_crop_x_ratio = 0.3
        self.box_crop_y_ratio = 0.7
        self.xy_center_point = False
        self.image_size = 128
        self.transforms = A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(),
            ToTensorV2(),
        ])
        
class rsna_saggital_mil_spinal_crop_x03_y05_t2_v4_auxloss(rsna_saggital_spinal_v2):
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv('sagittal_spinal_range2_rolling5_t2.csv')
        self.label_features = [
            'spinal_canal_stenosis_normal',
            'spinal_canal_stenosis_moderate',
            'spinal_canal_stenosis_severe',
            'spinal_canal_stenosis',
        ]
        self.drop_rate = 0.0
        self.drop_path_rate = 0.0        
        base_model = timm.create_model(self.model_name, pretrained=False, num_classes=1,
            drop_rate=self.drop_rate, drop_path_rate=self.drop_path_rate)
        self.model = RSNA2ndModel(
            base_model=base_model,
            num_classes=len(self.label_features)
        )
        
        d = '/kaggle/input/rsna-2024-reduce-noise-models/saggital-spinal-x03-y05-t2-reduce-noise-auxloss'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'

        self.box_crop = True
        self.box_crop_x_ratio = 0.3
        self.box_crop_y_ratio = 0.5
        self.xy_center_point = False
        self.image_size = 384
        self.batch_size = 1
        self.transforms = A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(),
            ToTensorV2(),
        ])
        
class rsna_saggital_mil_spinal_crop_x03_y07_t2_v4_auxloss(rsna_saggital_spinal_v2):
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv('sagittal_spinal_range2_rolling5_t2.csv')
        self.label_features = [
            'spinal_canal_stenosis_normal',
            'spinal_canal_stenosis_moderate',
            'spinal_canal_stenosis_severe',
            'spinal_canal_stenosis',
        ]
        self.drop_rate = 0.0
        self.drop_path_rate = 0.0        
        base_model = timm.create_model(self.model_name, pretrained=False, num_classes=1,
            drop_rate=self.drop_rate, drop_path_rate=self.drop_path_rate)
        self.model = RSNA2ndModel(
            base_model=base_model,
            num_classes=len(self.label_features)
        )
        
        self.box_crop = True
        self.box_crop_x_ratio = 0.3
        self.box_crop_y_ratio = 0.7
        self.xy_center_point = False
                                
        d = '/kaggle/input/rsna-2024-reduce-noise-models/saggital-spinal-x03-y07-t2-reduce-noise-auxloss'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'
        self.image_size = 384
        self.batch_size = 1
        self.transforms = A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(),
            ToTensorV2(),
        ])
        

class rsna_saggital_mil_crop_lr_nfn_model1_datav2(base):
    def __init__(self):
        super().__init__()
        left = pd.read_csv('sagittal_left_nfn_range2_rolling5.csv')
        left['left_right'] = 'left'
        right = pd.read_csv('sagittal_right_nfn_range2_rolling5.csv')
        right['left_right'] = 'right'
        self.df = pd.concat([left, right])

        self.label_features = [
            'neural_foraminal_narrowing_normal',
            'neural_foraminal_narrowing_moderate',
            'neural_foraminal_narrowing_severe',
        ]
        self.drop_rate = 0.0
        self.drop_path_rate = 0.0        
        base_model = timm.create_model(self.model_name, pretrained=False, num_classes=1,
            drop_rate=self.drop_rate, drop_path_rate=self.drop_path_rate)
        self.model = RSNA2ndModel(
            base_model=base_model,
            num_classes=len(self.label_features)
        )
        
        d = '/kaggle/input/rsna-2024-reduce-noise-models-v2/saggital-nfn-reduce-noise'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'

        self.image_size = 128
        self.transforms = A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(),
            ToTensorV2(),
        ])
        self.box_crop = None
        
class rsna_saggital_mil_nfn_crop_x07_y1_v2(rsna_saggital_mil_crop_lr_nfn_model1_datav2):
    def __init__(self):
        super().__init__()        
        self.box_crop = True
        self.box_crop_x_ratio = 0.7
        self.box_crop_y_ratio = 1.0
        d = '/kaggle/input/rsna-2024-reduce-noise-models-v2/saggital-nfn-x07-y1-reduce-noise'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'
        self.image_size = 160
        self.transforms = A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(),
            ToTensorV2(),
        ])
class rsna_saggital_mil_nfn_crop_x15_y1_v2(rsna_saggital_mil_crop_lr_nfn_model1_datav2):
    def __init__(self):
        super().__init__()        
        self.box_crop = True
        self.box_crop_x_ratio = 1.5
        self.box_crop_y_ratio = 1.0
        d = '/kaggle/input/rsna-2024-reduce-noise-models-v2/saggital-nfn-x15-y1-reduce-noise'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'
        self.image_size = 160
        self.transforms = A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(),
            ToTensorV2(),
        ])
class rsna_saggital_mil_nfn_crop_x03_y1_v2(rsna_saggital_mil_crop_lr_nfn_model1_datav2):
    def __init__(self):
        super().__init__()        
        self.box_crop = True
        self.box_crop_x_ratio = 0.3
        self.box_crop_y_ratio = 1.0
        d = '/kaggle/input/rsna-2024-reduce-noise-models-v2/saggital-nfn-x03-y1-reduce-noise'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'
        self.image_size = 160
        self.transforms = A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(),
            ToTensorV2(),
        ])
class rsna_saggital_mil_nfn_crop_x05_y05_v2(rsna_saggital_mil_crop_lr_nfn_model1_datav2):
    def __init__(self):
        super().__init__()        
        self.box_crop = True
        self.box_crop_x_ratio = 0.5
        self.box_crop_y_ratio = 0.5
        d = '/kaggle/input/rsna-2024-reduce-noise-models-v2/saggital-nfn-x05-y05-reduce-noise'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'
        self.image_size = 160
        self.transforms = A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(),
            ToTensorV2(),
        ])



class rsna_saggital_mil_ss_crop_x03_y05_96(base):
    def __init__(self):
        super().__init__()
        self.box_crop = True
        self.box_crop_x_ratio = 0.3
        self.box_crop_y_ratio = 0.5

        left = pd.read_csv('sagittal_left_ss_range2_rolling5.csv')
        left['left_right'] = 'left'
        right = pd.read_csv('sagittal_right_ss_range2_rolling5.csv')
        right['left_right'] = 'right'
        self.df = pd.concat([left, right])

        self.label_features = [
            'subarticular_stenosis_normal',
            'subarticular_stenosis_moderate',
            'subarticular_stenosis_severe',
        ]
        self.drop_rate = 0.0
        self.drop_path_rate = 0.0        
        base_model = timm.create_model(self.model_name, pretrained=False, num_classes=1,
            drop_rate=self.drop_rate, drop_path_rate=self.drop_path_rate)
        self.model = RSNA2ndModel(
            base_model=base_model,
            num_classes=len(self.label_features)
        )
        
        d = '/kaggle/input/rsna-2024-reduce-noise-models-v2/saggital-ss-x03-y05-reduce-noise-96'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'

        self.image_size = 96
        self.transforms = A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(),
            ToTensorV2(),
        ])
        
class rsna_saggital_mil_ss_crop_x03_y07_96(rsna_saggital_mil_ss_crop_x03_y05_96):
    def __init__(self):
        super().__init__()        
        self.box_crop = True
        self.box_crop_x_ratio = 0.3
        self.box_crop_y_ratio = 0.7
        d = '/kaggle/input/rsna-2024-reduce-noise-models-v2/saggital-ss-x03-y07-reduce-noise-96'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'
        self.image_size = 96
        self.transforms = A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(),
            ToTensorV2(),
        ])
        
class rsna_saggital_mil_ss_crop_x03_y2_96(rsna_saggital_mil_ss_crop_x03_y05_96):
    def __init__(self):
        super().__init__()        
        self.box_crop = True
        self.box_crop_x_ratio = 0.3
        self.box_crop_y_ratio = 2.0
        d = '/kaggle/input/rsna-2024-reduce-noise-models-v2/saggital-ss-x03-y2-reduce-noise-96'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'
        self.image_size = 96
        self.transforms = A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(),
            ToTensorV2(),
        ])
        
class rsna_saggital_mil_ss_crop_x1_y07_96(rsna_saggital_mil_ss_crop_x03_y05_96):
    def __init__(self):
        super().__init__()        
        self.box_crop = True
        self.box_crop_x_ratio = 1.0
        self.box_crop_y_ratio = 0.7
        d = '/kaggle/input/rsna-2024-reduce-noise-models-v2/saggital-ss-x1-y07-reduce-noise-96'
        if debug:
            self.model_paths = [f'{d}/last_fold{debug_fold}.ckpt' for fold in range(5)]
        else:
            self.model_paths = [f'{d}/last_fold{fold}.ckpt' for fold in range(5)]
        self.oof_path = f'{d}/oof_fold{debug_fold}.csv'
        self.image_size = 96
        self.transforms = A.Compose([
            A.Resize(self.image_size, self.image_size),
            A.Normalize(),
            ToTensorV2(),
        ])


# In[ ]:


import copy
config_names = [
'rsna_saggital_mil_spinal_crop_x03_y05',
'rsna_saggital_mil_spinal_crop_x03_y07',

'rsna_saggital_mil_ss_crop_x03_y05_96',
'rsna_saggital_mil_ss_crop_x03_y07_96',
'rsna_saggital_mil_ss_crop_x03_y2_96',
'rsna_saggital_mil_ss_crop_x1_y07_96',    
    
'rsna_saggital_mil_nfn_crop_x07_y1_v2',
'rsna_saggital_mil_nfn_crop_x15_y1_v2',
'rsna_saggital_mil_nfn_crop_x03_y1_v2',
'rsna_saggital_mil_nfn_crop_x05_y05_v2',      
]
for config_name in config_names:
    cfg = eval(config_name)()
    models = []
    for model_path in cfg.model_paths:
        state_dict = torch.load(model_path, map_location=torch.device('cpu'))
        model = copy.deepcopy(cfg.model)
        model.load_state_dict(state_dict)
        model.to(DEVICE)
        model.eval()
        models.append(model)


    ds = RSNA2024DatasetMIL(cfg)
    loader = DataLoader(ds, batch_size=cfg.batch_size, shuffle=False, drop_last=False, num_workers=4)
    preds = []
    for images in tqdm(loader, smoothing=0):
        images = images.to(DEVICE)
        batch_preds = []
        for model in models:
            batch_preds.append(model(images).detach().cpu().numpy())

        preds += np.mean(batch_preds, axis=0).tolist()
    pred_cols = [f'pred_{c}' for c in cfg.label_features]
    cfg.df[pred_cols] = np.array(preds)
    cfg.df.to_csv(f'{config_name}.csv', index=False)


# # aggregate predictions

# In[ ]:


# axial
def aggregate_axial_preds(configs, targets):
    cols = []
    pred_cols = []
    for target in targets:
        for c in ['normal', 'moderate', 'severe']:
            cols.append(f'pred_{target}_{c}')
            pred_cols.append(f'pred_{c}')
                
    preds = []
    for c in configs:
        df = pd.read_csv(f'{c}.csv')
        preds.append(df[cols].values)
        
    df[cols] = np.mean(preds, 0)

    if 'left_right' not in list(df):
        df['left_right'] = 'center'
    df = df[df.dis < 5]
    df = df.groupby(['study_id', 'pred_level', 'left_right'])[cols].mean().reset_index().sort_values(['study_id', 'pred_level', 'left_right'])
    df.columns = ['study_id', 'pred_level', 'left_right']+pred_cols
    
    return df

spinal_configs = [
    'rsna_axial_spinal_dis3_crop_x05_y6',
    'rsna_axial_spinal_dis3_crop_x1_y2',
]
axial_spinal = aggregate_axial_preds(spinal_configs, ['spinal_canal_stenosis'])

nfn_configs = [
    'rsna_axial_ss_nfn_x2_y2_center_pad0',
    'rsna_axial_ss_nfn_x2_y6_center_pad0',
    'rsna_axial_ss_nfn_x2_y8_center_pad10',
]
axial_nfn = aggregate_axial_preds(nfn_configs, ['neural_foraminal_narrowing'])

ss_configs = [
    'rsna_axial_ss_nfn_x2_y2_center_pad0',
    'rsna_axial_ss_nfn_x2_y6_center_pad0',
    'rsna_axial_ss_nfn_x2_y8_center_pad10',
]
axial_ss = aggregate_axial_preds(ss_configs, ['subarticular_stenosis'])
axial_spinal

# sagittal
def aggregate_sagittal_preds(configs, targets):
    cols = []
    pred_cols = []
    for target in targets:
        for c in ['normal', 'moderate', 'severe']:
            cols.append(f'pred_{target}_{c}')
            pred_cols.append(f'pred_{c}')
                
    preds = []
    for c in configs:
        df = pd.read_csv(f'{c}.csv')
        preds.append(df[cols].values)
        
    df[cols] = np.mean(preds, 0)
    if 'left_right' not in list(df):
        df['left_right'] = 'center'
    df = df.groupby(['study_id', 'level', 'left_right'])[cols].mean().reset_index().sort_values(['study_id', 'level', 'left_right'])
    df.columns = ['study_id', 'level', 'left_right']+pred_cols
    df['pred_level'] = df.level.map({
        'L1/L2': 1,
        'L2/L3': 2,
        'L3/L4': 3,
        'L4/L5': 4,
        'L5/S1': 5,
    })
    del df['level']
    return df

spinal_configs = [
    'rsna_saggital_mil_spinal_crop_x03_y05',
    'rsna_saggital_mil_spinal_crop_x03_y07',
]
sagittal_spinal = aggregate_sagittal_preds(spinal_configs, ['spinal_canal_stenosis'])

nfn_configs = [
    'rsna_saggital_mil_nfn_crop_x07_y1_v2',
    'rsna_saggital_mil_nfn_crop_x15_y1_v2',
    'rsna_saggital_mil_nfn_crop_x03_y1_v2',
    'rsna_saggital_mil_nfn_crop_x05_y05_v2',  
]
sagittal_nfn = aggregate_sagittal_preds(nfn_configs, ['neural_foraminal_narrowing'])

ss_configs = [
    'rsna_saggital_mil_ss_crop_x03_y05_96',
    'rsna_saggital_mil_ss_crop_x03_y07_96',
    'rsna_saggital_mil_ss_crop_x03_y2_96',
    'rsna_saggital_mil_ss_crop_x1_y07_96',
]
sagittal_ss = aggregate_sagittal_preds(ss_configs, ['subarticular_stenosis'])


# In[ ]:


study_ids = []
targets = []
levels = []
is_axials = []
level_preds = []
distances = []
lrs = []
trues = []
preds = []

for (study_id, level), idf in axial_spinal.groupby(['study_id', 'pred_level']):
    preds.append(idf[['pred_normal', 'pred_moderate', 'pred_severe']].mean(0).values)
    study_ids.append(study_id)
    targets.append('spinal')
    levels.append(level)
    is_axials.append(1)
    lrs.append('center')

for (study_id, level, lr), idf in axial_nfn.groupby(['study_id', 'pred_level', 'left_right']):
    preds.append(idf[['pred_normal', 'pred_moderate', 'pred_severe']].mean(0).values)
    study_ids.append(study_id)
    targets.append('nfn')
    levels.append(level)
    is_axials.append(1)
    lrs.append(lr)
for (study_id, level, lr), idf in axial_ss.groupby(['study_id', 'pred_level', 'left_right']):
    preds.append(idf[['pred_normal', 'pred_moderate', 'pred_severe']].mean(0).values)
    study_ids.append(study_id)
    targets.append('ss')
    levels.append(level)
    is_axials.append(1)
    lrs.append(lr)
for (study_id, level), idf in sagittal_spinal.groupby(['study_id', 'pred_level']):
    preds.append(idf[['pred_normal', 'pred_moderate', 'pred_severe']].mean(0).values)
    study_ids.append(study_id)
    targets.append('spinal')
    levels.append(level)
    is_axials.append(0)
    lrs.append('center')
for (study_id, level, lr), idf in sagittal_nfn.groupby(['study_id', 'pred_level', 'left_right']):
    preds.append(idf[['pred_normal', 'pred_moderate', 'pred_severe']].mean(0).values)
    study_ids.append(study_id)
    targets.append('nfn')
    levels.append(level)
    is_axials.append(0)
    lrs.append(lr)
for (study_id, level, lr), idf in sagittal_ss.groupby(['study_id', 'pred_level', 'left_right']):
    preds.append(idf[['pred_normal', 'pred_moderate', 'pred_severe']].mean(0).values)
    study_ids.append(study_id)
    targets.append('ss')
    levels.append(level)
    is_axials.append(0)
    lrs.append(lr)    
oof = pd.DataFrame({
    'study_id': study_ids,
    'target': targets,
    'level': levels,
    'is_axial': is_axials,
    'lr': lrs,
})
oof[['pred_normal', 'pred_moderate', 'pred_severe']] = np.array(preds)


# In[ ]:


axial = oof[oof.is_axial==1]
axial.head(2)
axial.columns = [
'study_id',
'target',
'level',
'is_axial',
'lr',
'axial_pred_normal',
'axial_pred_moderate',
'axial_pred_severe'
]
del axial['is_axial']

sagittal = oof[oof.is_axial==0]
sagittal.columns = [
'study_id',
'target',
'level',
'is_axial',
'lr',
'sagittal_pred_normal',
'sagittal_pred_moderate',
'sagittal_pred_severe']

del sagittal['is_axial']

df = axial.merge(sagittal, on=['study_id', 'target', 'level', 'lr'], how='outer')

df.loc[df.sagittal_pred_normal.isnull(), 'sagittal_pred_normal'] = df.loc[df.sagittal_pred_normal.isnull(), 'axial_pred_normal']
df.loc[df.sagittal_pred_moderate.isnull(), 'sagittal_pred_moderate'] = df.loc[df.sagittal_pred_moderate.isnull(), 'axial_pred_moderate']
df.loc[df.sagittal_pred_severe.isnull(), 'sagittal_pred_severe'] = df.loc[df.sagittal_pred_severe.isnull(), 'axial_pred_severe']

df.loc[df.axial_pred_normal.isnull(), 'axial_pred_normal'] = df.loc[df.axial_pred_normal.isnull(), 'sagittal_pred_normal']
df.loc[df.axial_pred_moderate.isnull(), 'axial_pred_moderate'] = df.loc[df.axial_pred_moderate.isnull(), 'sagittal_pred_moderate']
df.loc[df.axial_pred_severe.isnull(), 'axial_pred_severe'] = df.loc[df.axial_pred_severe.isnull(), 'sagittal_pred_severe']

df.loc[((df.target=='nfn') & (df.lr == 'left')), 'target'] = 'left_neural_foraminal_narrowing'
df.loc[((df.target=='nfn') & (df.lr == 'right')), 'target'] = 'right_neural_foraminal_narrowing'
df.loc[((df.target=='ss') & (df.lr == 'left')), 'target'] = 'left_subarticular_stenosis'
df.loc[((df.target=='ss') & (df.lr == 'right')), 'target'] = 'right_subarticular_stenosis'
df.loc[(df.target=='spinal'), 'target'] = 'spinal_canal_stenosis'
df.level = df.level.map({
    1: 'l1_l2',
    2: 'l2_l3',
    3: 'l3_l4',
    4: 'l4_l5',
    5: 'l5_s1',
})
df=df.sort_values(['study_id', 'target'])


# In[ ]:


m = {
    'study_id': []
}
meta_cols = []
for axial_sagittal in ['sagittal', 'axial']:
    for target in ['spinal_canal_stenosis', 'left_neural_foraminal_narrowing', 'right_neural_foraminal_narrowing', 'left_subarticular_stenosis', 'right_subarticular_stenosis']:
        for level in ['l1_l2', 'l2_l3', 'l3_l4', 'l4_l5', 'l5_s1']:
            for condition in ['normal', 'moderate', 'severe']:
                m[f'{axial_sagittal}_pred_{target}_{level}_{condition}'] = []
                meta_cols.append(f'{axial_sagittal}_pred_{target}_{level}_{condition}')
    
ts  = []
for i, idf in df.groupby('study_id'):
    m['study_id'].append(i)

    for level in ['l1_l2', 'l2_l3', 'l3_l4', 'l4_l5', 'l5_s1']:
        ldf = idf[idf.level == level]
        for target in ['spinal_canal_stenosis', 'left_neural_foraminal_narrowing', 'right_neural_foraminal_narrowing', 'left_subarticular_stenosis', 'right_subarticular_stenosis']:
            tdf = ldf[ldf.target == target]
            for condition in ['normal', 'moderate', 'severe']:
                
                for axial_sagittal in ['sagittal', 'axial']:
                    if len(tdf) == 0:
                        m[f'{axial_sagittal}_pred_{target}_{level}_{condition}'].append(np.nan)
                    else:
                        assert len(tdf) == 1
                        m[f'{axial_sagittal}_pred_{target}_{level}_{condition}'].append(tdf[f'{axial_sagittal}_pred_{condition}'].values[0])
df = pd.DataFrame(m)

# In[ ]:


def normalize_probabilities_to_one_torch(tensor: torch.Tensor) -> torch.Tensor:
    # Normalize the sum of each row's probabilities to 100%.
    # 0.75, 0.75 => 0.5, 0.5
    # 0.1, 0.1 => 0.5, 0.5
    row_totals = tensor.sum(dim=1, keepdim=True)
    if (row_totals == 0).any():
        return tensor
        raise ValueError('All rows must contain at least one non-zero prediction')
    normalized_tensor = tensor / row_totals
    return normalized_tensor
cols = ['spinal_canal_stenosis_l1_l2_normal', 'spinal_canal_stenosis_l1_l2_moderate', 'spinal_canal_stenosis_l1_l2_severe', 'left_neural_foraminal_narrowing_l1_l2_normal', 'left_neural_foraminal_narrowing_l1_l2_moderate', 'left_neural_foraminal_narrowing_l1_l2_severe', 'right_neural_foraminal_narrowing_l1_l2_normal', 'right_neural_foraminal_narrowing_l1_l2_moderate', 'right_neural_foraminal_narrowing_l1_l2_severe', 'left_subarticular_stenosis_l1_l2_normal', 'left_subarticular_stenosis_l1_l2_moderate', 'left_subarticular_stenosis_l1_l2_severe', 'right_subarticular_stenosis_l1_l2_normal', 'right_subarticular_stenosis_l1_l2_moderate', 'right_subarticular_stenosis_l1_l2_severe', 'spinal_canal_stenosis_l2_l3_normal', 'spinal_canal_stenosis_l2_l3_moderate', 'spinal_canal_stenosis_l2_l3_severe', 'left_neural_foraminal_narrowing_l2_l3_normal', 'left_neural_foraminal_narrowing_l2_l3_moderate', 'left_neural_foraminal_narrowing_l2_l3_severe', 'right_neural_foraminal_narrowing_l2_l3_normal', 'right_neural_foraminal_narrowing_l2_l3_moderate', 'right_neural_foraminal_narrowing_l2_l3_severe', 'left_subarticular_stenosis_l2_l3_normal', 'left_subarticular_stenosis_l2_l3_moderate', 'left_subarticular_stenosis_l2_l3_severe', 'right_subarticular_stenosis_l2_l3_normal', 'right_subarticular_stenosis_l2_l3_moderate', 'right_subarticular_stenosis_l2_l3_severe', 'spinal_canal_stenosis_l3_l4_normal', 'spinal_canal_stenosis_l3_l4_moderate', 'spinal_canal_stenosis_l3_l4_severe', 'left_neural_foraminal_narrowing_l3_l4_normal', 'left_neural_foraminal_narrowing_l3_l4_moderate', 'left_neural_foraminal_narrowing_l3_l4_severe', 'right_neural_foraminal_narrowing_l3_l4_normal', 'right_neural_foraminal_narrowing_l3_l4_moderate', 'right_neural_foraminal_narrowing_l3_l4_severe', 'left_subarticular_stenosis_l3_l4_normal', 'left_subarticular_stenosis_l3_l4_moderate', 'left_subarticular_stenosis_l3_l4_severe', 'right_subarticular_stenosis_l3_l4_normal', 'right_subarticular_stenosis_l3_l4_moderate', 'right_subarticular_stenosis_l3_l4_severe', 'spinal_canal_stenosis_l4_l5_normal', 'spinal_canal_stenosis_l4_l5_moderate', 'spinal_canal_stenosis_l4_l5_severe', 'left_neural_foraminal_narrowing_l4_l5_normal', 'left_neural_foraminal_narrowing_l4_l5_moderate', 'left_neural_foraminal_narrowing_l4_l5_severe', 'right_neural_foraminal_narrowing_l4_l5_normal', 'right_neural_foraminal_narrowing_l4_l5_moderate', 'right_neural_foraminal_narrowing_l4_l5_severe', 'left_subarticular_stenosis_l4_l5_normal', 'left_subarticular_stenosis_l4_l5_moderate', 'left_subarticular_stenosis_l4_l5_severe', 'right_subarticular_stenosis_l4_l5_normal', 'right_subarticular_stenosis_l4_l5_moderate', 'right_subarticular_stenosis_l4_l5_severe', 'spinal_canal_stenosis_l5_s1_normal', 'spinal_canal_stenosis_l5_s1_moderate', 'spinal_canal_stenosis_l5_s1_severe', 'left_neural_foraminal_narrowing_l5_s1_normal', 'left_neural_foraminal_narrowing_l5_s1_moderate', 'left_neural_foraminal_narrowing_l5_s1_severe', 'right_neural_foraminal_narrowing_l5_s1_normal', 'right_neural_foraminal_narrowing_l5_s1_moderate', 'right_neural_foraminal_narrowing_l5_s1_severe', 'left_subarticular_stenosis_l5_s1_normal', 'left_subarticular_stenosis_l5_s1_moderate', 'left_subarticular_stenosis_l5_s1_severe', 'right_subarticular_stenosis_l5_s1_normal', 'right_subarticular_stenosis_l5_s1_moderate', 'right_subarticular_stenosis_l5_s1_severe']
label_features = ['pred_'+c for c in cols]

ws = [0.7, 0.4, 0.8]
for condition, w in zip(['spinal', 'neural_foraminal_narrowing', 'subarticular_stenosis'], ws):    
    c_cols = [c for c in label_features if condition in c]
    for c in c_cols:
        df[c] = df['axial_'+c]*w + df['sagittal_'+c]*(1-w)

for c in label_features:
    df[c] = df[c].fillna(df[c].mean())

preds = sigmoid(df[label_features].values)
preds = torch.FloatTensor(preds)
for i in range(5):
    preds[:, i*3+1] *= 1.8
    preds[:, i*3+2] *= 5
    preds[:, i*3:(i+1)*3] = normalize_probabilities_to_one_torch(preds[:, i*3:(i+1)*3])
for i in range(5, 15):
    preds[:, i*3+1] *= 2.2
    preds[:, i*3+2] *= 5
    preds[:, i*3:(i+1)*3] = normalize_probabilities_to_one_torch(preds[:, i*3:(i+1)*3])
for i in range(15, 25):
    preds[:, i*3+1] *= 2.2
    preds[:, i*3+2] *= 5.5
    preds[:, i*3:(i+1)*3] = normalize_probabilities_to_one_torch(preds[:, i*3:(i+1)*3])
df[label_features] = preds.numpy()
df = df.sort_values('study_id')
df.head()

df[['study_id']+label_features]
my_sub = df.copy()

row_ids = []
preds = []
for i, row in my_sub.iterrows():
    for c in [c for c in cols if 'normal' in c]:
        c = c.replace('_normal', '')
        row_ids.append(f'{int(row.study_id)}_{c}')
        preds.append([
            row[f'pred_{c}_normal'],
            row[f'pred_{c}_moderate'],
            row[f'pred_{c}_severe'],
        ])
pred_df = pd.DataFrame({'row_id': row_ids})
pred_df[['normal_mild','moderate','severe']] = np.array(preds)
my_sub = pred_df.sort_values('row_id')
my_sub.to_csv('my_sub.csv', index=False)
sub = pd.read_csv('/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification/sample_submission.csv').sort_values('row_id')
sub = sub[~sub.row_id.isin(my_sub.row_id)]
sub['normal_mild'] = my_sub['normal_mild'].mean()
sub['moderate'] = my_sub['moderate'].mean()
sub['severe'] = my_sub['severe'].mean()
sub = pd.concat([sub, my_sub])

if not debug:
    os.system('rm -rf ./*')
    os.system('rm -rf /kaggle/temp')

sub.to_csv('yuji_submission.csv', index=False)

# In[ ]:


# !unlink /kaggle/working/timm

# In[ ]:


import torch
import gc
def free_gpu_and_ram():
    gc.collect()
    torch.cuda.empty_cache()

# In[ ]:


free_gpu_and_ram()

# In[ ]:


!nvidia-smi

# In[ ]:


import sys
import os
sys.path.append('/kaggle/input/random-data/')

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['KAGGLE_IS_COMPETITION_RERUN'] = 'true'

# Dir to store imgs
for path in ["/tmp/images"]:
    if not os.path.exists(path):
        os.mkdir(path)

# In[ ]:


import os
import shutil

def clean_working(directory_path: str = "/kaggle/working/"):
    """
    Clean kaggle output directory.
    """
    if os.path.exists(directory_path):
        for item in os.listdir(directory_path):
            if "submission" in item:
                continue
            item_path = os.path.join(directory_path, item)
            try:
                if os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception as e:
                pass
        print(f"All items in '{directory_path}' have been removed.")
    else:
        print(f"'{directory_path}' does not exist.")
                
        
clean_working()

# ## Notes
# 
# ### TODO
# 
# - Make sure study_id's with no SagT2 are still predicted..

# In[ ]:


import pandas as pd
import os

if os.getenv('KAGGLE_IS_COMPETITION_RERUN'):
    FOLD= 0
    df= pd.read_csv("/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification/test_series_descriptions.csv")
    df_all= df.copy()
else:
    FOLD= 0
    N_SAMPLES= 100
    cols= ['study_id', 'series_id', 'series_description'] 
    df= pd.read_csv("/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification/train_series_descriptions.csv")
    md= pd.read_csv("/kaggle/input/rsna-data/metadata.csv")
    if FOLD != -1:
        md= md.loc[md.fold == FOLD, :].head(N_SAMPLES)
    df= pd.merge(df[cols], md[cols], how="inner", on=cols).reset_index(drop=True)
    df_all= df.copy()

df= df[df.series_description != "Axial T2"]
display(df)

# ## Log Models

# In[ ]:


import glob
import json

MODEL_DIR= "/kaggle/input/rsna-models"
MODELS= {
    "S2": {
#         "stage1": glob.glob("{}/cfg_stage1_h*_{}_*".format(MODEL_DIR, FOLD)),
#         "stage2": glob.glob("{}/cfg_stage2_h*_{}_*".format(MODEL_DIR, FOLD)),
        "stage1": glob.glob("{}/cfg_stage1_h*".format(MODEL_DIR)),
        "stage2": glob.glob("{}/cfg_stage2_h*_-100_*".format(MODEL_DIR)),
    },
    "S1": {
#         "stage1": glob.glob("{}/cfg_stage1_s1_*_{}_*".format(MODEL_DIR, FOLD)),
#         "stage2": glob.glob("{}/cfg_stage2_s1_*_{}_*".format(MODEL_DIR, FOLD)),
        "stage1": glob.glob("{}/cfg_stage1_s1_*".format(MODEL_DIR)),
        "stage2": glob.glob("{}/cfg_stage2_s1_*_-100_*".format(MODEL_DIR)),
    },
}
print(json.dumps(MODELS, indent=4))

# ## Imports

# In[ ]:


from src.preprocess.rsna import RsnaProcessor

from src.configs.cfg_stage1_s1 import cfg as cfg_stage1_s1
from src.configs.cfg_stage2_s1 import cfg as cfg_stage2_s1
from src.configs.cfg_stage1 import cfg as cfg_stage1_s2
from src.configs.cfg_stage2 import cfg as cfg_stage2_s2

from src.data.dataset_stage1 import Stage1Dataset
from src.data.dataset_stage2 import Stage2Dataset

from src.data.utils import get_val_dataloader
from src.models.mil import (
    MILModel, MILOneHead, MILThreeHeads,
)

from src.modules.train_stage1 import run_eval as run_eval_stage1
from src.modules.train_stage2 import run_eval as run_eval_stage2


from src.modules.infer import (
    stage1_s1_preds,
    stage1_s2_preds,
    stage2_s1_preds,
    stage2_s2_preds,
)

# ## Stage 0

# In[ ]:


# Process slides
z= df.groupby('study_id')[['series_id', 'series_description']].apply(lambda x: x.to_dict('records')).reset_index().copy()
p= RsnaProcessor(
    df= z,
    coords= pd.DataFrame([]),
    stage = 1,
    img_size_stage1= 256,
    img_size_stage2= 128,
    percentiles= (1,99),
    in_dir="/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification", 
    out_dir="/tmp/images/stage1_128/",
    mode="test" if os.getenv('KAGGLE_IS_COMPETITION_RERUN') else "train",
    )
p.run()

# ## Stage 1

# In[ ]:


# S1
stage1_s1_preds(
    df= df,
    cfg= cfg_stage1_s1,
    wpaths= MODELS["S1"]["stage1"],
    img_dir= "/tmp/images/stage1_128/",
)

# S2
stage1_s2_preds(
    df= df,
    cfg= cfg_stage1_s2,
    wpaths= MODELS["S2"]["stage1"],
    img_dir= "/tmp/images/stage1_128/",
)

# ## Stage 2

# In[ ]:


fpaths= glob.glob("stage1*csv")
coords= pd.concat([pd.read_csv(_) for _ in fpaths], axis=0)
coords= coords.groupby(['series_id', 'level', 'side'])[['relative_x', 'relative_y']].mean().reset_index()
coords= coords.sort_values(["series_id", "level", "side"]).reset_index(drop=True)
coords= coords[["series_id", "level", "side", "relative_x", "relative_y"]]
clean_working()
print(coords.shape)

# In[ ]:


p= RsnaProcessor(
    df= z,
    coords= coords,
    stage = 2,
    img_size_stage1= 256,
    img_size_stage2= 128,
    percentiles= (1,99),
    in_dir="/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification",  
    out_dir= "/tmp/images/stage2_128/",
    mode= "test" if os.getenv('KAGGLE_IS_COMPETITION_RERUN') else "train",
    )
p.run()

# In[ ]:


# S1
stage2_s1_preds(
    df= df,
    cfg= cfg_stage2_s1,
    wpaths= MODELS["S1"]["stage2"],
    img_dir= "/tmp/images/stage2_128/",
    n_tta= 9,
)

# S2
stage2_s2_preds(
    df= df,
    cfg= cfg_stage2_s2,
    wpaths= MODELS["S2"]["stage2"],
    img_dir= "/tmp/images/stage2_128/",
    n_tta= 9,
)

# ## Combine

# In[ ]:


# Merge DFs
fpaths= glob.glob("/kaggle/working/stage2*.csv")
sub= pd.concat([pd.read_csv(os.path.join("/kaggle/working/", x)) for x in fpaths], axis=0)
sub= sub.groupby("row_id").mean().reset_index()
sub

# In[ ]:


import numpy as np
from copy import deepcopy

def insert_missing_rows(sub: pd.DataFrame):
    if os.getenv('KAGGLE_IS_COMPETITION_RERUN'):
        df_all= pd.read_csv("/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification/test_series_descriptions.csv")
    else:
        return sub

    label_cols= [
                'spinal_canal_stenosis_l1_l2', 'spinal_canal_stenosis_l2_l3', 'spinal_canal_stenosis_l3_l4', 
                'spinal_canal_stenosis_l4_l5', 'spinal_canal_stenosis_l5_s1', 'left_neural_foraminal_narrowing_l1_l2', 
                'left_neural_foraminal_narrowing_l2_l3', 'left_neural_foraminal_narrowing_l3_l4', 'left_neural_foraminal_narrowing_l4_l5', 
                'left_neural_foraminal_narrowing_l5_s1', 'right_neural_foraminal_narrowing_l1_l2', 'right_neural_foraminal_narrowing_l2_l3', 
                'right_neural_foraminal_narrowing_l3_l4', 'right_neural_foraminal_narrowing_l4_l5', 'right_neural_foraminal_narrowing_l5_s1', 
                'left_subarticular_stenosis_l1_l2', 'left_subarticular_stenosis_l2_l3', 'left_subarticular_stenosis_l3_l4', 
                'left_subarticular_stenosis_l4_l5', 'left_subarticular_stenosis_l5_s1', 'right_subarticular_stenosis_l1_l2', 
                'right_subarticular_stenosis_l2_l3', 'right_subarticular_stenosis_l3_l4', 'right_subarticular_stenosis_l4_l5', 
                'right_subarticular_stenosis_l5_s1',
            ]
    
    # Create dummy row
    row= deepcopy(sub.iloc[0])
    row.normal_mild= 1/3
    row.moderate= 1/3
    row.severe= 1/3
    
    # Check every row exists
    z= sub["row_id"].values
    arr= []
    for val in df_all["study_id"].unique():
        for col in label_cols:
            value= "{}_{}".format(val, col)
            if value not in z:
                row= deepcopy(row)
                row.row_id= value
                arr.append(row)
    
    # Add new rows
    sub= pd.concat([sub, pd.DataFrame(arr)], axis=0, ignore_index=True)
    sub= sub.sort_values("row_id").reset_index(drop=True)
    return sub
            
# sub= insert_missing_rows(sub)
sub.to_csv('submission1.csv', index=False)
display(sub)

# In[ ]:


free_gpu_and_ram()

# In[ ]:


if os.getenv('KAGGLE_IS_COMPETITION_RERUN'):
    clean_working("/tmp/images/")
    clean_working("/kaggle/working/")
    pass
else:
    
    # Remove rows that have no labels
    sol= pd.read_csv("/kaggle/input/rsna-data/study_id_labels.csv")
    sol= pd.merge(sol, sub["row_id"], how="inner", on="row_id")
    sub= pd.merge(sub, sol["row_id"], how="inner", on="row_id")

    sol= sol.sort_values("row_id").reset_index(drop=True)
    sub= sub.sort_values("row_id").reset_index(drop=True)

    weights= np.array([1.0, 2.0, 4.0])
    sol["sample_weight"]= weights[np.argmax(sol[['normal_mild', 'moderate', 'severe']], axis=1)]
    
    from src.metrics.metric import score
    import json
    d= score(solution= sol.copy(), submission= sub.copy(), row_id_column_name="row_id", any_severe_scalar=1.0)
    print(json.dumps(d, indent=4))

# # Ian's Part

# ## Install Packages

# In[ ]:


!pip install -qq /kaggle/working/python-packages/timm-0.9.10-py3-none-any.whl
import timm
timm.__version__

# In[ ]:


!cp -r /kaggle/input/python-packages /kaggle/working
!pip install -qq /kaggle/working/python-packages/pylibjpeg_libjpeg-1.3.4-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
!pip install -qq /kaggle/working/python-packages/pylibjpeg_openjpeg-1.3.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
!pip install -qq /kaggle/working/python-packages/pylibjpeg_rle-1.3.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
!pip install -qq /kaggle/working/python-packages/portalocker-2.8.2-py3-none-any.whl
!pip install -qq /kaggle/working/python-packages/iopath-0.1.9-py3-none-any.whl
!pip install -qq /kaggle/working/python-packages/av-10.0.0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
!pip install -qq /kaggle/working/python-packages/yacs-0.1.8-py3-none-any.whl
!pip install -qq /kaggle/working/python-packages/fvcore-0.1.5.post20220512/
!pip install -qq /kaggle/working/python-packages/parameterized-0.8.1-py2.py3-none-any.whl
!pip install -qq /kaggle/working/python-packages/pytorchvideo-0.1.5/
# !pip install -qq /kaggle/working/python-packages/timm-0.9.10-py3-none-any.whl
!pip install -qq /kaggle/working/python-packages/antlr4-python3-runtime-4.9.3/
!pip install -qq /kaggle/working/python-packages/monai-1.3.0-202310121228-py3-none-any.whl

!cp /kaggle/input/gdcm-conda-install/gdcm.tar /kaggle/working/
!tar -xzvf gdcm.tar
!conda install --offline /kaggle/working/gdcm/gdcm-2.8.9-py37h71b2a6d_0.tar.bz2

# ## Imports

# In[ ]:


import albumentations as A
import glob
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pydicom
import sys
import torch

from collections import defaultdict
from importlib import import_module
from sklearn.metrics import log_loss
from tqdm import tqdm

sys.path.insert(0, "/kaggle/input/rsna-lspine-src/skp")

# ## Functions

# In[ ]:


def load_model(checkpoint_path, cfg):
    cfg.pretrained = False
    print(f"Loading weights from {checkpoint_path} ...")
    wts = torch.load(checkpoint_path)["state_dict"]
    wts = {k.replace("model.", ""): v for k, v in wts.items()}
    model = import_module(f"models.{cfg.model}").Net(cfg)
    model.load_state_dict(wts)
    model = model.eval().cuda()
    return model


def convert_to_8bit(x):
    lower, upper = np.percentile(x, (1, 99))
    x = np.clip(x, lower, upper)
    x = x - np.min(x)
    x = x / np.max(x) 
    return (x * 255).astype("uint8")


def convert_world_space_to_pixel_space(dicom, x, y, z):
    sx, sy, sz = [float(_) for _ in dicom.ImagePositionPatient]
    o0, o1, o2, o3, o4, o5, = [float(_) for _ in dicom.ImageOrientationPatient]
    dx, dy = dicom.PixelSpacing
    dz = dicom.SpacingBetweenSlices
    #
    ax = np.array([o0, o1, o2])
    ay = np.array([o3, o4, o5])
    az = np.cross(ax, ay)
    #
    p = np.array([x-sx, y-sy, z-sz])
    px = np.dot(ax, p) / dx
    py = np.dot(ay, p) / dy
    pz = np.dot(az, p) / dz
    #
    return px, py, pz


def convert_pixel_space_to_world_space(dicom, x, y):
    sx, sy, sz = [float(_) for _ in dicom.ImagePositionPatient]
    o0, o1, o2, o3, o4, o5 = [float(_) for _ in dicom.ImageOrientationPatient]
    dx, dy = dicom.PixelSpacing
    wx = o0*dx*x + o3*dy*y + sx
    wy = o1*dx*x + o4*dy*y + sy
    wz = o2*dx*x + o5*dy*y + sz
    return wx, wy, wz


def get_axial_pz(sagittal_t2_coords, axial_t2_dicoms):
    sag_world_coords = {}
    for lvl in ["l1_l2", "l2_l3", "l3_l4", "l4_l5", "l5_s1"]:
        sag_world_coords[lvl] = convert_pixel_space_to_world_space(sagittal_t2_coords[f"{lvl}_dicom"], 
                                                                   sagittal_t2_coords[f"{lvl}_x"],
                                                                   sagittal_t2_coords[f"{lvl}_y"])
    axial_pz_list = []
    for each_dicom in axial_t2_dicoms:
        pz_list = []
        for lvl, (wx, wy, wz) in sag_world_coords.items():
            px, py, pz = convert_world_space_to_pixel_space(each_dicom, wx, wy, wz)
            pz_list.append(pz)
        axial_pz_list.append(np.asarray(pz_list))
    return np.stack(axial_pz_list)
        
            
def load_dicom_stack(dicom_folder, plane, reverse_sort=False, sort_by_instance=False, sagittal_t2_coords=None):
    dicom_files = glob.glob(os.path.join(dicom_folder, "*.dcm"))
    dicoms = [pydicom.dcmread(f) for f in dicom_files]
    # There was one axial T2 study where orientation was coronal but when I checked the images they were axial
    # So we should probably just trust the series description rather than determine orientation ourselves
    plane = {"sagittal": 0, "coronal": 1, "axial": 2}[plane.lower()]
    instances = np.asarray([int(d.InstanceNumber) for d in dicoms])
    positions = np.asarray([float(d.ImagePositionPatient[plane]) for d in dicoms])
    idx = np.argsort(positions)
    if sort_by_instance:
        # Sometimes for axial images sorting by instance is better than sorting by ImagePositionPatient2
        # Due to oblique slice acquisitions
        # Determine if instances are in reverse order from positions
        # Because we will still be sorting from CRANIAL->CAUDAL
        ascending = instances[idx[-1]] > instances[idx[0]]
        idx = np.argsort(instances)
        if not ascending:
            idx = idx[::-1]
    # If reverse_sort=True, then increasing array index will be from LEFT->RIGHT and CRANIAL->CAUDAL
    if reverse_sort:
        idx = idx[::-1]
    array_shapes = np.vstack([d.pixel_array.shape for d in dicoms])
    h, w = array_shapes[:, 0].max(), array_shapes[:, 1].max()
    # For some axial T2 series, the arrays are not all the same shape- resize if necessary
    resizer = A.Resize(height=h, width=w, p=1)
    array = [resizer(image=d.pixel_array.astype("float32"))["image"] for d in dicoms]
    array = np.stack(array)
    array = array[idx]
    sorted_dicom_files = [dicom_files[ii] for ii in idx]
    if isinstance(sagittal_t2_coords, dict):
        try:
            pz = get_axial_pz(sagittal_t2_coords, [dicoms[ii] for ii in idx])
        except Exception as e:
            print(e)
            pz = None
        return convert_to_8bit(array), sorted_dicom_files, pz
    return convert_to_8bit(array), sorted_dicom_files, None


def convert_probas_to_foramina_slice_indices(logits, arr_shape):
    # targets of interest are 0-9 for probas, 10-19 for dist
    assert logits.shape[1] == 20
    indices = np.argmax(logits[:, :10], 0)
    levels = ["l1_l2", "l2_l3", "l3_l4", "l4_l5", "l5_s1"]
    levels = [f"rt_{lvl}" for lvl in levels] + [f"lt_{lvl}" for lvl in levels]
    d = {}
    for idx, lvl in enumerate(levels):
        d[f"{lvl}_slice_index"] = indices[idx]
    return d


def convert_dists_to_foramina_slice_indices(logits, arr_shape):
    # targets of interest are 0-9 for probas, 10-19 for dist
    assert logits.shape[1] == 20
    indices = np.argmin(logits[:, 10:], 0)
    levels = ["l1_l2", "l2_l3", "l3_l4", "l4_l5", "l5_s1"]
    levels = [f"rt_{lvl}" for lvl in levels] + [f"lt_{lvl}" for lvl in levels]
    d = {}
    for idx, lvl in enumerate(levels):
        d[f"{lvl}_slice_index"] = indices[idx]
    return d


def convert_dists_to_spinal_slice_indices(logits, arr_shape):
    # targets of interest are 0-4 for probas, 5-9 for dist
    assert logits.shape[1] == 10
    indices = np.argmin(logits[:, 5:], 0)
    levels = ["l1_l2", "l2_l3", "l3_l4", "l4_l5", "l5_s1"]
    d = {}
    for idx, lvl in enumerate(levels):
        d[f"{lvl}_slice_index"] = indices[idx]
    return d
    

def convert_probas_to_subarticular_slice_indices(logits, arr_shape, thresh=0.2):
    # NOTE: SIGMOID ALREADY APPLIED
    # logits.shape = (num_images, 26)
    # targets of interest are 6-10, 11-15 for rt and lt subarticular for each level
    assert logits.shape[1] == 26
    rt_prob = logits[:, 6:11]
    lt_prob = logits[:, 11:16]
    rt_indices, rt_max_prob = np.argmax(rt_prob, 0), rt_prob.max(0)
    lt_indices, lt_max_prob = np.argmax(lt_prob, 0), lt_prob.max(0)
    levels = ["l1_l2", "l2_l3", "l3_l4", "l4_l5", "l5_s1"]
    d = {}
    for idx, lvl in enumerate(levels):
        if rt_max_prob[idx] >= thresh:
            d[f"rt_{lvl}_slice_index"] = rt_indices[idx]
        if lt_max_prob[idx] >= thresh:
            d[f"lt_{lvl}_slice_index"] = lt_indices[idx]
    return d


def crop_square_around_center(img, xc, yc, size_factor=0.15, crop_3d=False):
    img_shape = (img.shape[1], img.shape[2]) if crop_3d else (img.shape[0], img.shape[1])
    h, w = size_factor * img_shape[0], size_factor * img_shape[1]
    x1, y1 = xc - w / 2, yc - h / 2
    x2, y2 = x1 + w, y1 + h
    x1, y1, x2, y2 = [int(_) for _ in [x1, y1, x2, y2]]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(img_shape[1], x2), min(img_shape[0], y2)
    return img[:, y1:y2, x1:x2] if crop_3d else img[y1:y2, x1:x2]


def generate_multiaug_crops(arr, slice_index, x, y, size_factor, side, lvl, offset=0.0175, slice_stagger=1):
    if slice_stagger == 1:
        # Use 1 slice on either side
        slice_indices = [slice_index, 
                         max(0, slice_index - 1), 
                         min(len(arr) - 1, slice_index + 1)]
    elif slice_stagger == 2:
        # Use 2 slices on either side
        slice_indices = [slice_index, 
                         max(0, slice_index - 1), 
                         min(len(arr) - 1, slice_index + 1), 
                         max(0, slice_index - 2), 
                         min(len(arr) - 1, slice_index + 2)]
    else:
        raise Exception("`slice_stagger` must be 1 or 2")
    offset_x, offset_y = int(offset * arr.shape[2]), int(offset * arr.shape[1])
    xs = [x, x - offset_x, x + offset_x]
    ys = [y, y - offset_y, y + offset_y]
    crop_dict = defaultdict(list)
    for each_slice_index in slice_indices:
        for xi in xs:
            for yi in ys:
                crop_dict[f"{side}{lvl}"].append(crop_square_around_center(arr[each_slice_index], xi, yi, size_factor=size_factor))
    return crop_dict


def crop_using_coords_dict(arr, coords_dict, bilat=True, size_factor=0.15, offset=0.0175, slice_stagger=1):
    sides = ["rt_", "lt_"] if bilat else [""]
    crop_dict = {}
    for lvl in ["l1_l2", "l2_l3", "l3_l4", "l4_l5", "l5_s1"]:
        for side in sides:
            try:
                slice_index = coords_dict[f"{side}{lvl}_slice_index"]
                x = coords_dict[f"{side}{lvl}_x"]
                y = coords_dict[f"{side}{lvl}_y"]
                crop_dict.update(generate_multiaug_crops(arr, slice_index, x, y, size_factor=size_factor, side=side, lvl=lvl, offset=offset, slice_stagger=slice_stagger))
            except KeyError:
                # If a level does not exist (mainly for axial series), just skip
                continue
    return crop_dict


def generate_multiaug_crops_all_slices(arr, x, y, size_factor, side, lvl, offset=0.0175):
    offset_x, offset_y = int(offset * arr.shape[2]), int(offset * arr.shape[1])
    coords = [
              (x, y), 
              (x - offset_x, y - offset_y), 
              (x + offset_x, y + offset_y), 
              (x - offset_x, y + offset_y), 
              (x + offset_x, y - offset_y)
             ]
    crop_dict = defaultdict(list)
    for xi, yi in coords:
        tmp_crops = crop_square_around_center(arr, xi, yi, size_factor=size_factor, crop_3d=True)
        for tc in tmp_crops:
            crop_dict[f"{side}{lvl}"].append(tc)
    return crop_dict


def crop_using_coords_dict_all_slices(arr, coords_dict, bilat=True, size_factor=0.15, offset=0.0175):
    sides = ["rt_", "lt_"] if bilat else [""]
    crop_dict = {}
    for lvl in ["l1_l2", "l2_l3", "l3_l4", "l4_l5", "l5_s1"]:
        for side in sides:
            try:
                x = coords_dict[f"{side}{lvl}_x"]
                y = coords_dict[f"{side}{lvl}_y"]
                crop_dict.update(generate_multiaug_crops_all_slices(arr, x, y, size_factor=size_factor, side=side, lvl=lvl, offset=offset))
            except KeyError:
                continue
    return crop_dict


def normalize(x):
    return x / np.expand_dims(x.sum(1), axis=-1)

# ## Specify What To Run

# In[ ]:


SAG_T1_FORAMINAL = True
SAG_T2_SPINAL = True
AX_T2_SUBARTICULAR = True
AX_T2_SPINAL = True

# ## Load Models

# In[ ]:


MODELS_DIR = "/kaggle/input/rsna-lspine-models-v5-sub/"

# ### Foraminal (Sagittal T1)

# In[ ]:


if SAG_T1_FORAMINAL:
    cfg_file = "cfg000_sagittal_t1_foramina_slice_dist_level_seq_224"
    cfg = import_module(f"configs.{cfg_file}").cfg
    checkpoint_path = os.path.join(MODELS_DIR, "foramen_localizer_cls_fold0.pt")

    foramina_localizer_cls0 = {
        "cfg": cfg, "model": load_model(checkpoint_path, cfg)
    }
    
    cfg_file = "cfg000_sagittal_t1_foramina_slice_dist_level_seq_224"
    cfg = import_module(f"configs.{cfg_file}").cfg
    checkpoint_path = os.path.join(MODELS_DIR, "foramen_localizer_cls_fold1.pt")

    foramina_localizer_cls1 = {
        "cfg": cfg, "model": load_model(checkpoint_path, cfg)
    }
    
    cfg_file = "cfg000_sagittal_t1_regression"
    cfg = import_module(f"configs.{cfg_file}").cfg
    checkpoint_path = os.path.join(MODELS_DIR, "foramen_localizer_reg_fold0.pt")

    foramina_localizer_reg0 = {
        "cfg": cfg, "model": load_model(checkpoint_path, cfg)
    }
    
    cfg_file = "cfg000_sagittal_t1_regression"
    cfg = import_module(f"configs.{cfg_file}").cfg
    checkpoint_path = os.path.join(MODELS_DIR, "foramen_localizer_reg_fold1.pt")

    foramina_localizer_reg1 = {
        "cfg": cfg, "model": load_model(checkpoint_path, cfg)
    }
    
    foramina_stenosis_models = []
    
    cfg_file = "cfg000_genv4_foramen_crops_bb_bce_gt"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.backbone = "maxvit_tiny_tf_512"
    cfg.backbone_img_size = True
    checkpoint_path = os.path.join(MODELS_DIR, "foramen_stenosis_maxvit_fold0.pt")

    foramina_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg), 
        "name": "maxvit", "act_fn": "sigmoid", "aggregate": "median"
    })
    
    cfg_file = "cfg000_genv4_foramen_crops_bb_bce_gt"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.model = "net_csn_r101"
    cfg.num_input_channels = 1
    checkpoint_path = os.path.join(MODELS_DIR, "foramen_stenosis_csn_r101_fold1.pt")

    foramina_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg),
        "name": "csn_r101", "act_fn": "sigmoid", "aggregate": "median"
    })
    
    cfg_file = "cfg000_genv4_foramen_crops_bb_bce_gt_attn_pool"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.backbone = "coatnet_1_rw_224"
    cfg.backbone_img_size = True
    checkpoint_path = os.path.join(MODELS_DIR, "foramen_stenosis_coatnet_pool_fold2.pt")

    foramina_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg),
        "name": "coatnet_pool", "act_fn": "sigmoid", "aggregate": "median"
    })
    
    cfg_file = "cfg000_genv4_foramen_crops_bb_bce_gt_attn_pool"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.backbone = "maxvit_tiny_tf_512"
    cfg.backbone_img_size = True
    checkpoint_path = os.path.join(MODELS_DIR, "foramen_stenosis_maxvit_pool_fold3.pt")

    foramina_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg),
        "name": "maxvit_pool", "act_fn": "sigmoid", "aggregate": "median"
    })

# ### Spinal (Sagittal T2)

# In[ ]:


if SAG_T2_SPINAL:
    cfg_file = "cfg000_sagittal_t2_spinal_slice_dist_level_seq"
    cfg = import_module(f"configs.{cfg_file}").cfg
    checkpoint_path = os.path.join(MODELS_DIR, "spinal_sag_localizer_cls_fold0.pt")

    spinal_sag_localizer_cls0 = {
        "cfg": cfg, "model": load_model(checkpoint_path, cfg)
    }
    
    cfg_file = "cfg000_sagittal_t2_spinal_slice_dist_level_seq"
    cfg = import_module(f"configs.{cfg_file}").cfg
    checkpoint_path = os.path.join(MODELS_DIR, "spinal_sag_localizer_cls_fold1.pt")

    spinal_sag_localizer_cls1 = {
        "cfg": cfg, "model": load_model(checkpoint_path, cfg)
    }
    
    cfg_file = "cfg000_sagittal_t2_regression"
    cfg = import_module(f"configs.{cfg_file}").cfg
    checkpoint_path = os.path.join(MODELS_DIR, "spinal_sag_localizer_reg_fold0.pt")

    spinal_sag_localizer_reg0 = {
        "cfg": cfg, "model": load_model(checkpoint_path, cfg)
    }
    
    cfg_file = "cfg000_sagittal_t2_regression"
    cfg = import_module(f"configs.{cfg_file}").cfg
    checkpoint_path = os.path.join(MODELS_DIR, "spinal_sag_localizer_reg_fold1.pt")

    spinal_sag_localizer_reg1 = {
        "cfg": cfg, "model": load_model(checkpoint_path, cfg)
    }
    
    spinal_sag_stenosis_models = []
    
    cfg_file = "cfg000_genv5_spinal_crops_gt_half"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.backbone = "maxvit_tiny_tf_512"
    cfg.backbone_img_size = True
    checkpoint_path = os.path.join(MODELS_DIR, "spinal_sag_stenosis_maxvit_all_fold0.pt")

    spinal_sag_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg), 
        "name": "maxvit_all", "act_fn": "sigmoid", "aggregate": "mean"
    })
    
    cfg_file = "cfg000_genv5_spinal_crops_gt_half"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.backbone = "tiny_vit_21m_512.dist_in22k_ft_in1k"
    cfg.backbone_img_size = False
    checkpoint_path = os.path.join(MODELS_DIR, "spinal_sag_stenosis_tinyvit_all_fold1.pt")

    spinal_sag_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg),
        "name": "tinyvit_all", "act_fn": "sigmoid", "aggregate": "mean"
    })
    
    cfg_file = "cfg000_genv5_spinal_crops_gt_half"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.model = "net_csn_r101"
    cfg.num_input_channels = 1
    cfg.backbone_img_size = False
    checkpoint_path = os.path.join(MODELS_DIR, "spinal_sag_stenosis_csn_r101_all_fold2.pt")

    spinal_sag_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg),
        "name": "csn_r101_all", "act_fn": "sigmoid", "aggregate": "mean"
    })
    
    cfg_file = "cfg000_genv5_spinal_crops_gt_half_attn_pool"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.backbone = "maxvit_tiny_tf_512"
    cfg.backbone_img_size = True
    checkpoint_path = os.path.join(MODELS_DIR, "spinal_sag_stenosis_maxvit_pool_all_fold3.pt")

    spinal_sag_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg),
        "name": "maxvit_pool_all", "act_fn": "sigmoid", "aggregate": "mean"
    })
    
    cfg_file = "cfg000_genv5_spinal_crops_gt_half_attn_pool"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.backbone = "tf_efficientnetv2_m"
    cfg.backbone_img_size = False
    checkpoint_path = os.path.join(MODELS_DIR, "spinal_sag_stenosis_effnet_pool_all_fold4.pt")

    spinal_sag_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg),
        "name": "effnet_pool_all", "act_fn": "sigmoid", "aggregate": "mean"
    })

# ### Axial T2 Localizers

# In[ ]:


if AX_T2_SUBARTICULAR or AX_T2_SPINAL:

    cfg_file = "cfg000_axial_subarticular_slice_dist_level_seq"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.backbone = "resnet18d"
    checkpoint_path = os.path.join(MODELS_DIR, "ax_localizer_cls_old_resnet_fold0.pt")
    
    ax_localizer_cls_old = {
        "cfg": cfg, "model": load_model(checkpoint_path, cfg)
    }


    cfg_file = "cfg000_axial_subarticular_slice_dist_level_seq_v2"
    cfg = import_module(f"configs.{cfg_file}").cfg
    checkpoint_path = os.path.join(MODELS_DIR, "ax_localizer_cls_resnet_fold0.pt")
    
    ax_localizer_cls1 = {
        "cfg": cfg, "model": load_model(checkpoint_path, cfg)
    }
    
    cfg_file = "cfg000_axial_subarticular_slice_dist_level_seq_v2"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.backbone = "tinynet_c"
    checkpoint_path = os.path.join(MODELS_DIR, "ax_localizer_cls_tinynet_fold1.pt")
    
    ax_localizer_cls2 = {
        "cfg": cfg, "model": load_model(checkpoint_path, cfg)
    }

    cfg_file = "cfg000_axial_subarticular_slice_dist_level_seq_v2"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.backbone = "mobilenetv3_large_100"
    checkpoint_path = os.path.join(MODELS_DIR, "ax_localizer_cls_mobilenet_fold2.pt")
    
    ax_localizer_cls3 = {
        "cfg": cfg, "model": load_model(checkpoint_path, cfg)
    }

    cfg_file = "cfg000_axial_t2_regression"
    cfg = import_module(f"configs.{cfg_file}").cfg
#     checkpoint_path = "/kaggle/input/rsna-lspine-models-v4-sub/ax_localizer_reg_fold0.pt")
    checkpoint_path = os.path.join(MODELS_DIR, "ax_localizer_reg_fold0.pt")
    
    ax_localizer_reg1 = {
        "cfg": cfg, "model": load_model(checkpoint_path, cfg)
    }

    cfg_file = "cfg000_axial_t2_regression"
    cfg = import_module(f"configs.{cfg_file}").cfg
    checkpoint_path = os.path.join(MODELS_DIR, "ax_localizer_reg_fold1.pt")
    
    ax_localizer_reg2 = {
        "cfg": cfg, "model": load_model(checkpoint_path, cfg)
    }

# ### Subarticular (Axial T2)

# In[ ]:


if AX_T2_SUBARTICULAR:
    subarticular_stenosis_models = []
    
    cfg_file = "cfg000_genv4_subarticular_crops_bb_bce_gt"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.model = "net_2d"
    cfg.num_input_channels = 3
    cfg.backbone = "dm_nfnet_f0.dm_in1k"
    cfg.backbone_img_size = False
    checkpoint_path = os.path.join(MODELS_DIR, "subarticular_stenosis_nfnet_fold0.pt")

    subarticular_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg),
        "name": "nfnet", "act_fn": "sigmoid", "aggregate": "median"
    })
    
    cfg_file = "cfg000_genv4_subarticular_crops_bb_bce_gt"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.model = "net_csn_r101"
    cfg.num_input_channels = 1
    checkpoint_path = os.path.join(MODELS_DIR, "subarticular_stenosis_csn_r101_fold1.pt")

    subarticular_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg),
        "name": "csn_r101", "act_fn": "sigmoid", "aggregate": "median"
    })
    
    cfg_file = "cfg000_gen5_subarticular_crops_5ch_clam"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.backbone = "maxvit_tiny_tf_512"
    cfg.backbone_img_size = True
    checkpoint_path = os.path.join(MODELS_DIR, "subarticular_stenosis_maxvit_clam_fold2.pt")

    subarticular_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg), 
        "name": "maxvit_clam", "act_fn": "sigmoid", "aggregate": "mean"
    })

    cfg_file = "cfg000_gen5_subarticular_crops_5ch_clam_xcit"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.backbone = "xcit_tiny_12_p8_384.fb_dist_in1k"
    checkpoint_path = os.path.join(MODELS_DIR, "subarticular_stenosis_xcit_clam_fold3.pt")

    subarticular_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg),
        "name": "xcit_clam", "act_fn": "sigmoid", "aggregate": "mean"
    })

# ### Spinal (Axial T2)

# In[ ]:


if AX_T2_SPINAL:
    spinal_ax_stenosis_models = []
    
    cfg_file = "cfg000_genv5_axial_spinal_crops_bb_bce_gt"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.model = "net_2d"
    cfg.num_input_channels = 3
    cfg.backbone = "maxvit_tiny_tf_512"
    cfg.backbone_img_size = True
    checkpoint_path = os.path.join(MODELS_DIR, "spinal_ax_stenosis_maxvit_fold0.pt")

    spinal_ax_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg),
        "name": "maxvit", "act_fn": "sigmoid", "aggregate": "mean"
    })
    
    cfg_file = "cfg000_genv5_axial_spinal_crops_bb_bce_gt"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.backbone = "coatnet_1_rw_224"
    cfg.backbone_img_size = True
    checkpoint_path = os.path.join(MODELS_DIR, "spinal_ax_stenosis_coatnet_fold1.pt")

    spinal_ax_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg),
        "name": "coatnet", "act_fn": "sigmoid", "aggregate": "mean"
    })
    
    cfg_file = "cfg000_genv5_axial_spinal_crops_bb_bce_gt"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.backbone = "tiny_vit_21m_512.dist_in22k_ft_in1k"
    cfg.backbone_img_size = False
    checkpoint_path = os.path.join(MODELS_DIR, "spinal_ax_stenosis_tinyvit_fold2.pt")

    spinal_ax_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg),
        "name": "tinyvit", "act_fn": "sigmoid", "aggregate": "mean"
    })
    
    cfg_file = "cfg000_genv5_axial_spinal_crops_bb_bce_gt"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.model = "net_csn_r101"
    cfg.num_input_channels = 1
    cfg.backbone_img_size = False
    checkpoint_path = os.path.join(MODELS_DIR, "spinal_ax_stenosis_csn_r101_fold3.pt")

    spinal_ax_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg),
        "name": "csn_r101", "act_fn": "sigmoid", "aggregate": "mean"
    })
 
    cfg_file = "cfg000_genv5_axial_spinal_crops_bb_bce_gt_attn_pool"
    cfg = import_module(f"configs.{cfg_file}").cfg
    cfg.backbone = "coatnet_1_rw_224"
    cfg.backbone_img_size = True
    checkpoint_path = os.path.join(MODELS_DIR, "spinal_ax_stenosis_coatnet_pool_fold4.pt")

    spinal_ax_stenosis_models.append({
        "cfg": cfg, "model": load_model(checkpoint_path, cfg),
        "name": "coatnet_pool", "act_fn": "sigmoid", "aggregate": "mean"
    })

# ## Load Data Info

# In[ ]:


description_df = pd.read_csv("/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification/test_series_descriptions.csv")
study_series_id_description_dict = {f"{row.study_id}-{row.series_id}": row.series_description for row in description_df.itertuples()}
dicom_dir = "/kaggle/input/rsna-2024-lumbar-spine-degenerative-classification/test_images"
all_study_ids = os.listdir(dicom_dir)

# ## Run Inference

# In[ ]:


levels = ["l1_l2", "l2_l3", "l3_l4", "l4_l5", "l5_s1"]
levels_dict = {lvl: ii for ii, lvl in enumerate(levels)}
levels_lat = [f"rt_{lvl}" for lvl in levels] + [f"lt_{lvl}" for lvl in levels]

foramina_stenosis_preds_by_study = {}
spinal_sag_stenosis_preds_by_study = {}
subarticular_stenosis_preds_by_study = {}
spinal_ax_stenosis_preds_by_study = {}

for study_id in tqdm(all_study_ids, total=len(all_study_ids)):

    # --- FIND AVAILABLE SERIES --- #
    series = glob.glob(os.path.join(dicom_dir, str(study_id), "*"))
    series_path_dict = defaultdict(list)
    for each_series in series:
        series_path_dict[study_series_id_description_dict[f"{study_id}-{os.path.basename(each_series)}"]].append(each_series)

    # --- BEGIN FORAMINAL --- #
    SAG_T1_AVAILABLE = len(series_path_dict["Sagittal T1"]) > 0
    # A few studies had multiple sagittal T1 series
    # Upon manual review, it seems that they were all duplicates of each other
    # So we should be fine just taking any of them
    if SAG_T1_AVAILABLE and SAG_T1_FORAMINAL:
        sag_t1 = series_path_dict["Sagittal T1"][0]
        sag_t1, sag_t1_dicom_files, _ = load_dicom_stack(sag_t1, plane="sagittal")

    foramina_stenosis_preds = defaultdict(dict)
    
    if SAG_T1_AVAILABLE and SAG_T1_FORAMINAL:
        # Create 3-channel stacked volume # (N, H, W) -> (N, H, W, 3)
        sag_t1 = np.stack([
            np.concatenate([np.expand_dims(sag_t1[0], axis=0), sag_t1[:-1]]),
            sag_t1,
            np.concatenate([sag_t1[1:], np.expand_dims(sag_t1[-1], axis=0)])
        ], axis=-1)

        # Get slice indices and coordinates for each side/level 
        sag_t1_torch = np.stack([foramina_localizer_cls1["cfg"].val_transforms(image=_)["image"] for _ in sag_t1])
        sag_t1_torch = sag_t1_torch.transpose(0, 3, 1, 2)
        sag_t1_torch = torch.from_numpy(sag_t1_torch).float().to("cuda:0").unsqueeze(0)
        with torch.inference_mode():
            out1 = foramina_localizer_cls0["model"]({"x": sag_t1_torch})["logits"][0].cpu().abs().numpy()
            out2 = foramina_localizer_cls1["model"]({"x": sag_t1_torch})["logits"][0].cpu().abs().numpy()
        
        out = (out1 + out2) / 2.0
        
        coords_dict = convert_dists_to_foramina_slice_indices(out, arr_shape=sag_t1.shape[1:])
        store_coords_preds = {}
        for k, v in coords_dict.copy().items():
            tmp_sag_t1_torch = foramina_localizer_reg1["cfg"].val_transforms(image=sag_t1[v], keypoints=[])["image"]
            tmp_sag_t1_torch = torch.from_numpy(tmp_sag_t1_torch).permute(2, 0, 1).unsqueeze(0).float().to("cuda:0")
            if v in store_coords_preds:
                # If coordinates were already predicted for that slice
                # No need to predict again
                coords = store_coords_preds[v]
            else:
                with torch.inference_mode():
                    reg_out1 = foramina_localizer_reg0["model"]({"x": tmp_sag_t1_torch})["logits"].sigmoid().cpu().numpy()[0]
                    reg_out2 = foramina_localizer_reg1["model"]({"x": tmp_sag_t1_torch})["logits"].sigmoid().cpu().numpy()[0]
                
                reg_out = (reg_out1 + reg_out2) / 2.0
                coords = np.stack([reg_out[:5], reg_out[5:]], axis=1)
                store_coords_preds[v] = coords
            x, y = coords[levels_dict[k.replace("_slice_index", "")[3:]]]
            coords_dict[k.replace("slice_index", "x")] = x * sag_t1.shape[2]
            coords_dict[k.replace("slice_index", "y")] = y * sag_t1.shape[1]

        # Generate multiple crops
        foramina_crops = crop_using_coords_dict(sag_t1, coords_dict, bilat=True, size_factor=0.15)

        # Run 2D crop-aggregate models
        for k, v in foramina_crops.items():
            # All backbones use same val_transforms (resize to 64 x 64)
            v = np.stack([foramina_stenosis_models[0]["cfg"].val_transforms(image=_crop)["image"] for _crop in v])
            v = torch.from_numpy(v.transpose(0, 3, 1, 2)).float().to("cuda:0")
            out_list = []
            for model_idx, each_model in enumerate(foramina_stenosis_models):
                
                with torch.inference_mode():
                    if each_model["name"].startswith("csn_r101"):
                        # For 3D CSN need to unsqueeze 3rd spatial dimension
                        tmp_out = each_model["model"]({"x": v.unsqueeze(1)})
                    else:
                        tmp_out = each_model["model"]({"x": v})
                    
                if each_model["act_fn"] == "sigmoid":
                    tmp_out = tmp_out["logits"].sigmoid().cpu().numpy()
                elif each_model["act_fn"] == "softmax": 
                    tmp_out = torch.softmax(tmp_out["logits"], dim=1).cpu().numpy()

                if each_model["aggregate"] == "median":
                    tmp_out = np.median(tmp_out, axis=0)
                elif each_model["aggregate"] == "mean":
                    tmp_out = np.mean(tmp_out, axis=0)

                foramina_stenosis_preds[k][each_model["name"]] = tmp_out
            
    if SAG_T1_FORAMINAL:
        # Fill in missing levels
        for each_lvl in levels_lat:
            if each_lvl not in [*foramina_stenosis_preds]:
                for each_model in foramina_stenosis_models:
                    foramina_stenosis_preds[each_lvl][each_model["name"]] = np.asarray([1/3., 1/3., 1/3.])
                    
        foramina_stenosis_preds_by_study[study_id] = foramina_stenosis_preds

    # --- END FORAMINAL --- #

    # --- BEGIN SPINAL (SAG T2) --- #
    SAG_T2_AVAILABLE = len(series_path_dict["Sagittal T2/STIR"]) > 0
    # If more than 1 sagittal T2 series, just take the first one
    if SAG_T2_AVAILABLE and SAG_T2_SPINAL:
        sag_t2 = series_path_dict["Sagittal T2/STIR"][0]
        sag_t2_series = os.path.basename(sag_t2)
        sag_t2, sag_t2_dicom_files, _ = load_dicom_stack(sag_t2, plane="sagittal")
    
    sagittal_t2_coords_for_axial = None
    
    spinal_sag_stenosis_preds = defaultdict(dict)
    
    if SAG_T2_AVAILABLE and SAG_T2_SPINAL:
        # Create 3-channel stacked volume # (N, H, W) -> (N, H, W, 3)
        sag_t2 = np.stack([
            np.concatenate([np.expand_dims(sag_t2[0], axis=0), sag_t2[:-1]]),
            sag_t2,
            np.concatenate([sag_t2[1:], np.expand_dims(sag_t2[-1], axis=0)])
        ], axis=-1)

        # Get slice indices and coordinates for each side/level 
        sag_t2_torch = np.stack([spinal_sag_localizer_cls1["cfg"].val_transforms(image=_)["image"] for _ in sag_t2])
        sag_t2_torch = sag_t2_torch.transpose(0, 3, 1, 2)
        sag_t2_torch = torch.from_numpy(sag_t2_torch).float().to("cuda:0").unsqueeze(0)
        with torch.inference_mode():
            out1 = spinal_sag_localizer_cls0["model"]({"x": sag_t2_torch})["logits"][0].cpu().abs().numpy()
            out2 = spinal_sag_localizer_cls1["model"]({"x": sag_t2_torch})["logits"][0].cpu().abs().numpy()
        
        out = (out1 + out2) / 2.0
        coords_dict = convert_dists_to_spinal_slice_indices(out, arr_shape=sag_t2.shape[1:])
        store_coords_preds = {}
        for k, v in coords_dict.copy().items():
            tmp_sag_t2_torch = spinal_sag_localizer_reg1["cfg"].val_transforms(image=sag_t2[v], keypoints=[])["image"]
            tmp_sag_t2_torch = torch.from_numpy(tmp_sag_t2_torch).permute(2, 0, 1).unsqueeze(0).float().to("cuda:0")
            if v in store_coords_preds:
                # If coordinates were already predicted for that slice
                # No need to predict again
                coords = store_coords_preds[v]
            else:
                with torch.inference_mode():
                    reg_out1 = spinal_sag_localizer_reg0["model"]({"x": tmp_sag_t2_torch})["logits"].sigmoid().cpu().numpy()[0]
                    reg_out2 = spinal_sag_localizer_reg1["model"]({"x": tmp_sag_t2_torch})["logits"].sigmoid().cpu().numpy()[0]
                
                reg_out = (reg_out1 + reg_out2) / 2.0
                coords = np.stack([reg_out[:5], reg_out[5:]], axis=1)
                store_coords_preds[v] = coords
            x, y = coords[levels_dict[k.replace("_slice_index", "")]]
            coords_dict[k.replace("slice_index", "x")] = x * sag_t2.shape[2]
            coords_dict[k.replace("slice_index", "y")] = y * sag_t2.shape[1]

        # Generate multiple crops
        spinal_sag_crops = crop_using_coords_dict(sag_t2, coords_dict, bilat=False, size_factor=0.15)
        spinal_sag_crops_all_slices = crop_using_coords_dict_all_slices(sag_t2, coords_dict, bilat=False, size_factor=0.15)
        
        # Assemble sagittal T2 coords for axial model
        sagittal_t2_coords_for_axial = coords_dict.copy()
        for k, v in sagittal_t2_coords_for_axial.copy().items():
            if k.endswith("slice_index"):
                sagittal_t2_coords_for_axial[k.replace("slice_index", "dicom")] = pydicom.dcmread(sag_t2_dicom_files[v], stop_before_pixels=True)

        # Run 2D crop-aggregate models
        for k, v in spinal_sag_crops.items():
            # All backbones use same val_transforms (resize to 64 x 64)
            v = np.stack([spinal_sag_stenosis_models[0]["cfg"].val_transforms(image=_crop)["image"] for _crop in v])
            v = torch.from_numpy(v.transpose(0, 3, 1, 2)).float().to("cuda:0")
            out_list = []
            for model_idx, each_model in enumerate(spinal_sag_stenosis_models):
                
                with torch.inference_mode():
                    if each_model["name"].startswith("csn_r101"):
                            # For 3D CSN need to unsqueeze 3rd spatial dimension
                        tmp_out = each_model["model"]({"x": v.unsqueeze(1)})["logits"]
                    else:
                        tmp_out = each_model["model"]({"x": v})["logits"]
                        
                if each_model["name"].endswith("_all"):
                    valid_slice_pred = tmp_out[:, 3].sigmoid().cpu().numpy()
                    valid_slices = np.where(valid_slice_pred >= 0.5)[0]
                    if len(valid_slices) == 0:
                        valid_slices = np.ascontiguousarray(np.argsort(valid_slice_pred)[::-1][:5])
                    tmp_out = tmp_out[valid_slices, :3]
                        
                if each_model["act_fn"] == "sigmoid":
                    tmp_out = tmp_out.sigmoid().cpu().numpy()
                elif each_model["act_fn"] == "softmax": 
                    tmp_out = torch.softmax(tmp_out, dim=1).cpu().numpy()

                if each_model["aggregate"] == "median":
                    tmp_out = np.median(tmp_out, axis=0)
                elif each_model["aggregate"] == "mean":
                    tmp_out = np.mean(tmp_out, axis=0)

                spinal_sag_stenosis_preds[k][each_model["name"]] = tmp_out


    if SAG_T2_SPINAL:
        # Fill in missing levels
        for each_lvl in levels:
            if each_lvl not in [*spinal_sag_stenosis_preds]:
                for each_model in spinal_sag_stenosis_models:
                    spinal_sag_stenosis_preds[each_lvl][each_model["name"]] = np.asarray([1/3., 1/3., 1/3.])
                    
        spinal_sag_stenosis_preds_by_study[study_id] = spinal_sag_stenosis_preds

    # --- END SPINAL (SAG T2) --- #

    # --- BEGIN SUBARTICULAR (+/- SPINAL AX T2) --- #
    AX_T2_AVAILABLE = len(series_path_dict["Axial T2"]) > 0
    # Some studies split axial T2s into segments 
    # So we  need to load all the available axial series
    if AX_T2_AVAILABLE and (AX_T2_SUBARTICULAR or AX_T2_SPINAL):
        ax_t2 = series_path_dict["Axial T2"]
        ax_t2 = {
            each_ax_t2: load_dicom_stack(each_ax_t2, 
                                         plane="axial", 
                                         sort_by_instance=True, 
                                         sagittal_t2_coords=sagittal_t2_coords_for_axial) 
            for each_ax_t2 in ax_t2
        }
        
    subarticular_stenosis_preds = defaultdict(dict)
    spinal_ax_stenosis_preds = defaultdict(dict)
    
    if AX_T2_AVAILABLE and (AX_T2_SUBARTICULAR or AX_T2_SPINAL):
        # Loop over series
        subarticular_crops_over_series = {}
        subarticular_crops_5ch_over_series = {}
        spinal_ax_crops_over_series = {}
        
        for each_ax_t2_series, (each_ax_t2, each_ax_t2_dicom_files, pz) in ax_t2.items():
            
            # Create 5-channel stacked volume # (N, H, W) -> (N, H, W, 5)
            each_ax_t2_5ch = np.stack([
                np.concatenate([np.expand_dims(each_ax_t2[0], axis=0), np.expand_dims(each_ax_t2[0], axis=0), each_ax_t2[:-2]]),
                np.concatenate([np.expand_dims(each_ax_t2[0], axis=0), each_ax_t2[:-1]]),
                each_ax_t2,
                np.concatenate([each_ax_t2[1:], np.expand_dims(each_ax_t2[-1], axis=0)]),
                np.concatenate([each_ax_t2[2:], np.expand_dims(each_ax_t2[-1], axis=0), np.expand_dims(each_ax_t2[-1], axis=0)])
            ], axis=-1)
            
            # Create 3-channel stacked volume # (N, H, W) -> (N, H, W, 3)
            each_ax_t2 = np.stack([
                np.concatenate([np.expand_dims(each_ax_t2[0], axis=0), each_ax_t2[:-1]]),
                each_ax_t2,
                np.concatenate([each_ax_t2[1:], np.expand_dims(each_ax_t2[-1], axis=0)])
            ], axis=-1)

            # Get slice indices and coordinates for each side/level 
            if isinstance(pz, np.ndarray):
                each_ax_t2_torch = np.stack([ax_localizer_cls1["cfg"].val_transforms(image=_)["image"] for _ in each_ax_t2])
                each_ax_t2_torch = each_ax_t2_torch.transpose(0, 3, 1, 2)
                each_ax_t2_torch = torch.from_numpy(each_ax_t2_torch).float().to("cuda:0").unsqueeze(0)
                pz = torch.from_numpy(pz).float().to("cuda:0").unsqueeze(0)
                with torch.inference_mode():
                    out1 = ax_localizer_cls1["model"]({"x": each_ax_t2_torch, "pz": pz})["logits"][0].cpu().sigmoid().numpy()
                    out2 = ax_localizer_cls2["model"]({"x": each_ax_t2_torch, "pz": pz})["logits"][0].cpu().sigmoid().numpy()
                    out3 = ax_localizer_cls3["model"]({"x": each_ax_t2_torch, "pz": pz})["logits"][0].cpu().sigmoid().numpy()
                    out = (out1 + out2 + out3) / 3.0
            else:
                each_ax_t2_torch = np.stack([ax_localizer_cls_old["cfg"].val_transforms(image=_)["image"] for _ in each_ax_t2])
                each_ax_t2_torch = each_ax_t2_torch.transpose(0, 3, 1, 2)
                each_ax_t2_torch = torch.from_numpy(each_ax_t2_torch).float().to("cuda:0").unsqueeze(0)
                with torch.inference_mode():
                    out = ax_localizer_cls_old["model"]({"x": each_ax_t2_torch})["logits"][0].cpu().sigmoid().numpy()
            
            coords_dict = convert_probas_to_subarticular_slice_indices(out, arr_shape=each_ax_t2.shape[1:], thresh=0.1)
            store_coords_preds = {}
            for k, v in coords_dict.copy().items():
                tmp_ax_t2_torch = ax_localizer_reg1["cfg"].val_transforms(image=each_ax_t2[v], keypoints=[])["image"]
                tmp_ax_t2_torch = torch.from_numpy(tmp_ax_t2_torch).permute(2, 0, 1).unsqueeze(0).float().to("cuda:0")
                with torch.inference_mode():
                    reg_out1 = ax_localizer_reg1["model"]({"x": tmp_ax_t2_torch})["logits"].sigmoid().cpu().numpy()[0]
                    reg_out2 = ax_localizer_reg2["model"]({"x": tmp_ax_t2_torch})["logits"].sigmoid().cpu().numpy()[0]
                
                reg_out = (reg_out1 + reg_out2) / 2.0
                if k.startswith("rt_"):
                    x, y = reg_out[:2]
                elif k.startswith("lt_"):
                    x, y = reg_out[2:]
                coords_dict[k.replace("slice_index", "x")] = x * each_ax_t2.shape[2]
                coords_dict[k.replace("slice_index", "y")] = y * each_ax_t2.shape[1]

            if AX_T2_SUBARTICULAR:
                subarticular_crops = crop_using_coords_dict(each_ax_t2, coords_dict, bilat=True, size_factor=0.125, slice_stagger=1)
                for k, v in subarticular_crops.items():
                    if k in subarticular_crops_over_series:
                        subarticular_crops_over_series[k].extend(v)
                    else:
                        subarticular_crops_over_series[k] = v
                        
                subarticular_crops_5ch = crop_using_coords_dict(each_ax_t2_5ch, coords_dict, bilat=True, size_factor=0.125, slice_stagger=1)
                for k, v in subarticular_crops_5ch.items():
                    if k in subarticular_crops_5ch_over_series:
                        subarticular_crops_5ch_over_series[k].extend(v)
                    else:
                        subarticular_crops_5ch_over_series[k] = v
                        
            if AX_T2_SPINAL:
                spinal_ax_coords_dict = {}
                # Edit coordinates for spinal
                for lvl in levels:
                    try:
                        spinal_ax_coords_dict[f"{lvl}_slice_index"] = (coords_dict[f"rt_{lvl}_slice_index"] + coords_dict[f"lt_{lvl}_slice_index"]) // 2
                        spinal_ax_coords_dict[f"{lvl}_x"] = (coords_dict[f"rt_{lvl}_x"] + coords_dict[f"lt_{lvl}_x"]) / 2
                        spinal_ax_coords_dict[f"{lvl}_y"] = 1.05 * ((coords_dict[f"rt_{lvl}_y"] + coords_dict[f"lt_{lvl}_y"]) / 2)
                    except KeyError:
                        # If level doesn't exist, just skip
                        continue
                spinal_ax_crops = crop_using_coords_dict(each_ax_t2, spinal_ax_coords_dict, bilat=False, size_factor=0.15, slice_stagger=1)
                for k, v in spinal_ax_crops.items():
                    if k in spinal_ax_crops_over_series:
                        spinal_ax_crops_over_series[k].extend(v)
                    else:
                        spinal_ax_crops_over_series[k] = v
                    
        # Run 2D crop-aggregate models
        if AX_T2_SUBARTICULAR:
            for k, v in subarticular_crops_over_series.items():
                # All backbones use same val_transforms (resize to 64 x 64)
                v = np.stack([subarticular_stenosis_models[0]["cfg"].val_transforms(image=_crop)["image"] for _crop in v])
                v = torch.from_numpy(v.transpose(0, 3, 1, 2)).float().to("cuda:0")
                out_list = []
                for model_idx, each_model in enumerate(subarticular_stenosis_models):
                    
                    if each_model["name"].endswith("_clam"):
                        continue

                    with torch.inference_mode():
                        if each_model["name"].startswith("csn_r101"):
                            # For 3D CSN need to unsqueeze 3rd spatial dimension
                            tmp_out = each_model["model"]({"x": v.unsqueeze(1)})
                        else:
                            tmp_out = each_model["model"]({"x": v})
                        
                    if each_model["act_fn"] == "sigmoid":
                        tmp_out = tmp_out["logits"].sigmoid().cpu().numpy()
                    elif each_model["act_fn"] == "softmax": 
                        tmp_out = torch.softmax(tmp_out["logits"], dim=1).cpu().numpy()
    
                    if each_model["aggregate"] == "median":
                        tmp_out = np.median(tmp_out, axis=0)
                    elif each_model["aggregate"] == "mean":
                        tmp_out = np.mean(tmp_out, axis=0)
    
                    subarticular_stenosis_preds[k][each_model["name"]] = tmp_out
        
            for k, v in subarticular_crops_5ch_over_series.items():
                # All backbones use same val_transforms (resize to 64 x 64)
                v = np.stack([subarticular_stenosis_models[-1]["cfg"].val_transforms(image=_crop)["image"] for _crop in v])
                v = torch.from_numpy(v.transpose(0, 3, 1, 2)).float().to("cuda:0")
                out_list = []
                for model_idx, each_model in enumerate(subarticular_stenosis_models):

                    if not each_model["name"].endswith("_clam"):
                        continue
                    
                    with torch.inference_mode():
                        if each_model["name"].startswith("csn_r101"):
                            # For 3D CSN need to unsqueeze 3rd spatial dimension
                            tmp_out = each_model["model"]({"x": v.unsqueeze(1)})
                        else:
                            tmp_out = each_model["model"]({"x": v})
                        
                    if each_model["act_fn"] == "sigmoid":
                        tmp_out = tmp_out["logits"].sigmoid().cpu().numpy()
                    elif each_model["act_fn"] == "softmax": 
                        tmp_out = torch.softmax(tmp_out["logits"], dim=1).cpu().numpy()
    
                    if each_model["aggregate"] == "median":
                        tmp_out = np.median(tmp_out, axis=0)
                    elif each_model["aggregate"] == "mean":
                        tmp_out = np.mean(tmp_out, axis=0)
    
                    subarticular_stenosis_preds[k][each_model["name"]] = tmp_out
        
        if AX_T2_SPINAL:
            for k, v in spinal_ax_crops_over_series.items():
                v = np.stack([spinal_ax_stenosis_models[0]["cfg"].val_transforms(image=_crop)["image"] for _crop in v])
                v = torch.from_numpy(v.transpose(0, 3, 1, 2)).float().to("cuda:0")
                out_list = []
                for model_idx, each_model in enumerate(spinal_ax_stenosis_models):
                    
                    with torch.inference_mode():
                        if each_model["name"].startswith("csn_r101"):
                            # For 3D CSN need to unsqueeze 3rd spatial dimension
                            tmp_out = each_model["model"]({"x": v.unsqueeze(1)})
                        else:
                            tmp_out = each_model["model"]({"x": v})
                        
                    if each_model["act_fn"] == "sigmoid":
                        tmp_out = tmp_out["logits"].sigmoid().cpu().numpy()
                    elif each_model["act_fn"] == "softmax": 
                        tmp_out = torch.softmax(tmp_out["logits"], dim=1).cpu().numpy()
    
                    if each_model["aggregate"] == "median":
                        tmp_out = np.median(tmp_out, axis=0)
                    elif each_model["aggregate"] == "mean":
                        tmp_out = np.mean(tmp_out, axis=0)
    
                    spinal_ax_stenosis_preds[k][each_model["name"]] = tmp_out
            
    if AX_T2_SUBARTICULAR:
        # Fill in missing levels
        # Note: Do NOT fill in missing levels for axial T2 spinal, since we will just use sagittal predictions
        #       instead of averaging
        for each_lvl in levels_lat:
            if each_lvl not in [*subarticular_stenosis_preds]:
                for each_model in subarticular_stenosis_models:
                    subarticular_stenosis_preds[each_lvl][each_model["name"]] = np.asarray([1/3., 1/3., 1/3.])
                    
        subarticular_stenosis_preds_by_study[study_id] = subarticular_stenosis_preds

    if AX_T2_SPINAL:
        spinal_ax_stenosis_preds_by_study[study_id] = spinal_ax_stenosis_preds

# ## Assemble Predictions

# ### Foraminal

# In[ ]:


if SAG_T1_FORAMINAL:
    df_dict = {}
    for model_idx, each_model in enumerate(foramina_stenosis_models):
        study_id_list, level_list, proba_list = [], [], []
        for study_id, stenosis_preds in foramina_stenosis_preds_by_study.items():
            for level, probas in stenosis_preds.items():
                study_id_list.append(study_id)
                level_list.append(level)
                proba_list.append(probas[each_model["name"]])
        tmp_df = pd.DataFrame(np.stack(proba_list))
        tmp_df.columns = ["normal_mild", "moderate", "severe"]
        tmp_df["study_id"] = study_id_list
        tmp_df["side_level"] = level_list
        tmp_df["backbone"] = each_model["name"]
        tmp_df["level"] = tmp_df.side_level.apply(lambda x: x[3:].upper())
        tmp_df["laterality"] = tmp_df.side_level.apply(lambda x: x[0].upper())
        df_dict[model_idx] = tmp_df

    pred_df = pd.concat([v for v in df_dict.values()])
    grades = ["normal_mild", "moderate", "severe"]
    pred_df[grades] = normalize(pred_df[grades].values)

    foramina_pred_df = pred_df.loc[pred_df.backbone == pred_df.backbone.unique()[0]].copy()
    for bb in pred_df.backbone.unique()[1:]:
        foramina_pred_df[grades] += pred_df.loc[pred_df.backbone == bb][grades].values

    foramina_pred_df[grades] /= len(pred_df.backbone.unique())
    print(foramina_pred_df.head())

# ### Spinal (Sagittal)

# In[ ]:


if SAG_T2_SPINAL:
    df_dict = {}
    for model_idx, each_model in enumerate(spinal_sag_stenosis_models):
        study_id_list, level_list, proba_list = [], [], []
        for study_id, stenosis_preds in spinal_sag_stenosis_preds_by_study.items():
            for level, probas in stenosis_preds.items():
                study_id_list.append(study_id)
                level_list.append(level)
                proba_list.append(probas[each_model["name"]])
        tmp_df = pd.DataFrame(np.stack(proba_list))
        tmp_df.columns = ["normal_mild", "moderate", "severe"]
        tmp_df["study_id"] = study_id_list
        tmp_df["backbone"] = each_model["name"]
        tmp_df["level"] = [_.upper() for _ in level_list]
        df_dict[model_idx] = tmp_df

    pred_df = pd.concat([v for v in df_dict.values()])
    grades = ["normal_mild", "moderate", "severe"]
    pred_df[grades] = normalize(pred_df[grades].values)

    spinal_sag_pred_df = pred_df.loc[pred_df.backbone == pred_df.backbone.unique()[0]].copy()
    for bb in pred_df.backbone.unique()[1:]:
        spinal_sag_pred_df[grades] += pred_df.loc[pred_df.backbone == bb][grades].values

    spinal_sag_pred_df[grades] /= len(pred_df.backbone.unique())

    print(spinal_sag_pred_df.head())

# ### Subarticular

# In[ ]:


if AX_T2_SUBARTICULAR:
    df_dict = {}
    for model_idx, each_model in enumerate(subarticular_stenosis_models):
        study_id_list, level_list, proba_list = [], [], []
        for study_id, stenosis_preds in subarticular_stenosis_preds_by_study.items():
            for level, probas in stenosis_preds.items():
                study_id_list.append(study_id)
                level_list.append(level)
                proba_list.append(probas[each_model["name"]])
        tmp_df = pd.DataFrame(np.stack(proba_list))
        tmp_df.columns = ["normal_mild", "moderate", "severe"]
        tmp_df["study_id"] = study_id_list
        tmp_df["side_level"] = level_list
        tmp_df["backbone"] = each_model["name"]
        tmp_df["level"] = tmp_df.side_level.apply(lambda x: x[3:].upper())
        tmp_df["laterality"] = tmp_df.side_level.apply(lambda x: x[0].upper())
        df_dict[model_idx] = tmp_df

    pred_df = pd.concat([v for v in df_dict.values()])
    grades = ["normal_mild", "moderate", "severe"]
    pred_df[grades] = normalize(pred_df[grades].values)

    subarticular_pred_df = pred_df.loc[pred_df.backbone == pred_df.backbone.unique()[0]].copy()
    for bb in pred_df.backbone.unique()[1:]:
        subarticular_pred_df[grades] += pred_df.loc[pred_df.backbone == bb][grades].values

    subarticular_pred_df[grades] /= len(pred_df.backbone.unique())
    print(subarticular_pred_df.head())

# ### Spinal (Axial)

# In[ ]:


if AX_T2_SPINAL:
    df_dict = {}
    for model_idx, each_model in enumerate(spinal_ax_stenosis_models):
        study_id_list, level_list, proba_list = [], [], []
        for study_id, stenosis_preds in spinal_ax_stenosis_preds_by_study.items():
            for level, probas in stenosis_preds.items():
                study_id_list.append(study_id)
                level_list.append(level)
                proba_list.append(probas[each_model["name"]])
        tmp_df = pd.DataFrame(np.stack(proba_list))
        tmp_df.columns = ["normal_mild", "moderate", "severe"]
        tmp_df["study_id"] = study_id_list
        tmp_df["backbone"] = each_model["name"]
        tmp_df["level"] = [_.upper() for _ in level_list]
        df_dict[model_idx] = tmp_df

    pred_df = pd.concat([v for v in df_dict.values()])
    grades = ["normal_mild", "moderate", "severe"]
    pred_df[grades] = normalize(pred_df[grades].values)

    spinal_ax_pred_df = pred_df.loc[pred_df.backbone == pred_df.backbone.unique()[0]].copy()
    for bb in pred_df.backbone.unique()[1:]:
        spinal_ax_pred_df[grades] += pred_df.loc[pred_df.backbone == bb][grades].values

    spinal_ax_pred_df[grades] /= len(pred_df.backbone.unique())

    print(spinal_ax_pred_df.head())

# ### Combine Spinal Sagittal and Axial

# In[ ]:


spinal_sag_pred_df["study_level"] = spinal_sag_pred_df.study_id.astype("str") + "_" + spinal_sag_pred_df.level
spinal_ax_pred_df["study_level"] = spinal_ax_pred_df.study_id.astype("str") + "_" + spinal_ax_pred_df.level

spinal_sag_missing_ax = spinal_sag_pred_df.loc[~spinal_sag_pred_df.study_level.isin(spinal_ax_pred_df.study_level.tolist())]
spinal_sag_present_ax = spinal_sag_pred_df.loc[spinal_sag_pred_df.study_level.isin(spinal_ax_pred_df.study_level.tolist())]

spinal_sag_present_ax = spinal_sag_present_ax.sort_values("study_level").reset_index(drop=True)
spinal_ax_pred_df = spinal_ax_pred_df.sort_values("study_level").reset_index(drop=True)

assert len(spinal_sag_present_ax) == len(spinal_ax_pred_df)
assert np.sum(spinal_sag_present_ax.study_level == spinal_ax_pred_df.study_level) == len(spinal_sag_present_ax)

weights = [1, 0.5]
spinal_sag_ax_ensemble = spinal_sag_present_ax.copy()
spinal_sag_ax_ensemble[grades] = (weights[0] * spinal_sag_present_ax[grades].values + weights[1] * spinal_ax_pred_df[grades].values) / np.sum(weights)
spinal_sag_ax_ensemble = pd.concat([spinal_sag_ax_ensemble, spinal_sag_missing_ax])

print(spinal_sag_ax_ensemble.head())

# In[ ]:


side_dict = {"L": "left", "R": "right"}
foramina_pred_df["row_id"] = foramina_pred_df.study_id.astype("str") + "_" + foramina_pred_df.laterality.map(side_dict) + \
                            "_neural_foraminal_narrowing_" + foramina_pred_df.level.apply(lambda x: x.lower())
foramina_pred_df = foramina_pred_df[["row_id", "normal_mild", "moderate", "severe"]]

spinal_sag_ax_ensemble["row_id"] = spinal_sag_ax_ensemble.study_id.astype("str") + "_spinal_canal_stenosis_" + \
                           spinal_sag_ax_ensemble.level.apply(lambda x: x.lower())
spinal_sag_ax_ensemble = spinal_sag_ax_ensemble[["row_id", "normal_mild", "moderate", "severe"]]

subarticular_pred_df["row_id"] = subarticular_pred_df.study_id.astype("str") + "_" + subarticular_pred_df.laterality.map(side_dict) + \
                                 "_subarticular_stenosis_" + subarticular_pred_df.level.apply(lambda x: x.lower())
subarticular_pred_df = subarticular_pred_df[["row_id", "normal_mild", "moderate", "severe"]]

submission = pd.concat([foramina_pred_df, spinal_sag_ax_ensemble, subarticular_pred_df]).sort_values("row_id")

# In[ ]:


submission.to_csv("submission2.csv", index=False)

# In[ ]:


!rm -rf python-packages
!rm -rf gdcm*

# ## Combine Submissions

# In[ ]:


sub1 = pd.read_csv("submission1.csv")
sub2 = pd.read_csv("submission2.csv")

sub1 = sub1.sort_values("row_id")
sub2 = sub2.sort_values("row_id")

# In[ ]:


sub1 = pd.read_csv("submission1.csv")
sub2 = pd.read_csv("submission2.csv")
yuji_sub = pd.read_csv('yuji_submission.csv')

sub = pd.concat([sub1, sub2, sub2, yuji_sub, yuji_sub]) # 1:2:2
# sub = pd.concat([sub1, sub1, sub1, sub2, sub2, sub2, sub2, sub2, yuji_sub, yuji_sub, yuji_sub, yuji_sub, yuji_sub]) # 3:5:5
# sub = pd.concat([sub1, sub1, sub2, sub2, sub2, sub2, sub2, yuji_sub, yuji_sub, yuji_sub, yuji_sub, yuji_sub]) # 2:5:5

sub = sub.groupby("row_id").mean().reset_index()

sub = insert_missing_rows(sub)

# In[ ]:


sub.to_csv("submission_before_pp.csv", index=False)

# In[ ]:


sub

# In[ ]:


def normalize_probabilities_to_one_numpy(array: np.ndarray) -> np.ndarray:
    total = np.sum(array)
    normalized_array = array / total
    return normalized_array

th = 0

sub['study_id'] = sub.row_id.apply(lambda x: int(x.split('_')[0]))
dfs = []
for id, idf in sub.groupby('study_id'):
    spinal = idf[idf.row_id.str.contains('spinal')]
    spinal_severe_max_val = spinal.severe.max()
    if spinal_severe_max_val > th:
        max_severe_row_id = spinal[spinal.severe == spinal_severe_max_val].row_id.values[0]
        idf.loc[idf.row_id == max_severe_row_id, 'severe'] *= 1.25
        vals = idf.loc[idf.row_id == max_severe_row_id, ['normal_mild', 'moderate', 'severe']].values[0]
        idf.loc[idf.row_id == max_severe_row_id, ['normal_mild', 'moderate', 'severe']] = normalize_probabilities_to_one_numpy(vals)
    dfs.append(idf)

sub_pp = pd.concat(dfs)
del sub_pp['study_id']

# In[ ]:


sub_pp.to_csv("submission.csv", index=False)

# In[ ]:


sub_pp

# In[ ]:



