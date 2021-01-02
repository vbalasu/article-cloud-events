jupyter nbconvert --to html README.ipynb
pandoc -o README.docx README.html
rm README.html
echo "README.docx created"

