#!/bin/bash
#SBATCH --job-name=sn_suppcheck
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=0-00:15:00
#SBATCH --output=suppcheck-%j.out
# Compile packet_src/supplement_technical.tex alone, in the manuscript's style file, without touching main.* or
# supplement.* (another workflow owns those). Output goes to packet_src/texcheck/.
# Submit: sbatch -D ~/spinesurg-ct-nnunet/SchwingNet/packet_src/texcheck ~/spinesurg-ct-nnunet/SchwingNet/packet_src/texcheck/check.sh
set -u
cd "$HOME/spinesurg-ct-nnunet/SchwingNet" || exit 1
echo "CHECK_START $(date) host=$(hostname)"
[ -f /etc/profile.d/modules.sh ] && . /etc/profile.d/modules.sh
[ -f /usr/share/Modules/init/bash ] && . /usr/share/Modules/init/bash
module load texlive/2020 > /dev/null 2>&1; echo "module rc=$?"
[ -f localfont.tex ] && echo "localfont: $(cat localfont.tex)" || echo "no localfont.tex (compile.sh writes it)"
OUT=packet_src/texcheck
rm -f $OUT/supp_technical_check.{aux,log,pdf,out,xdv}
for pass in 1 2; do
  xelatex -interaction=nonstopmode -halt-on-error -output-directory=$OUT $OUT/supp_technical_check.tex > $OUT/pass$pass.log 2>&1
  echo "pass $pass rc=$?"
done
L=$OUT/supp_technical_check.log
grep -a -o 'Output written on [^ ]* ([0-9]* page[s]*' $L | sed 's/^/PDF /'
grep -a -c 'LaTeX Warning' $L | sed 's/^/latex_warnings /'
grep -a 'LaTeX Warning' $L | head -10
grep -a -c 'Overfull' $L | sed 's/^/overfull /'
grep -a -A2 'Overfull' $L | head -12
grep -a -A4 '^!' $L | head -30
echo "CHECK_END $(date)"
