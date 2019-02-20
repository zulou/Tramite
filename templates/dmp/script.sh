
path=1
for file in *.html
do
 filename=$(basename "$file")
 sed -i -e 's/127.0.0.1/157.230.59.200/g' $file

done