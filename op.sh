eval $(op signin)

echo 'Search'
read searchterm


op list items |jq -c '.[]' - | while read i
do

    name=$(echo $i | jq  .overview.title| tr -d '"')
    if  [[ "$name" =~  "$searchterm" ]]
    then
        uuid=$(echo $i | jq  .uuid| tr -d '"')
        values=$(op get item $uuid)
        url=$(echo $values | jq .overview.url| tr -d '"')
        username=$(echo $values | jq .details.fields | jq -c '.[]' - | while read j
        do
            if [[ $(echo $j | jq .type | tr -d '"') == "T" ]]
            then
                  echo $j | jq .value | tr -d '"'
            fi
        done
        )
        password=$(echo $values | jq .details.fields | jq -c '.[]' - | while read j
        do
            if [[ $(echo $j | jq .type | tr -d '"') == "P" ]]
            then
                  echo $j | jq .value | tr -d '"'
            fi
        done
        )
        echo -e " ${name}\t${username}\t${password}\t${url}" | awk '{ printf "%-30s %-25s %-25s %-25s\n", $1, $2, $3, $4} '
    fi
done
read  -n 1
