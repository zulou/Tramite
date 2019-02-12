
for file in *.js
do
 filename=$(basename "$file")
 sed -i 's/address=.*/address='$addr'/' $file

done