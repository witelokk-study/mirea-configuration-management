TEXT=$1;

TEXT_LENGTH=$(expr length "$1");

function print_border {
    printf "+";
    for ((i=1;i<=$TEXT_LENGTH+2;i++));
    do
        printf "-"
    done;
    printf "+\n"
}

print_border;
echo "| $1 |";
print_border;
