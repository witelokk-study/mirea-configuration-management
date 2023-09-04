FIRST_LINE=$(cat $1 | head -n 1)

if { [[ $1 == *".py" ]] && $(echo $FIRST_LINE | grep -q "^ *#"); } \
|| { [[ $1 == *".c" ]] && $(echo $FIRST_LINE | grep -q -e "//.\+" -e "/*.\+\*/"); } \
|| { [[ $1 == *".js" ]] && $(echo $FIRST_LINE | grep -q -e "//.\+"); }; then
    echo "comment found";
else
    echo "comment not found"
fi