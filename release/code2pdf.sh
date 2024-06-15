# please pass $1 var like this.
# "file1 file2 file3 ...."

cat -n $1 | paps --header --landscape --columns=2 --font=9 > result.ps
ps2pdf result.ps
