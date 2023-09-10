files=$(find . -type f)

for file in $files; do
    for file2 in $files; do
        if [[ "$file" == "$file2" ]]; then
            continue;
        fi
        if [[ $( cat $file2 ) == *$(cat $file)* ]]; then
            echo "duplicates $file $file2";
        fi;
    done
done