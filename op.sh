eval $(op signin)

echo 'Search'
read searchterm


op list items |jq -c '.[]' - | while read i
do
    name=$(echo $i | jq  .overview.title| tr -d '"')
    if  [[ "$name" =~  "$searchterm" ]]
    then
        echo ''
        uuid=$(echo $i | jq  .uuid| tr -d '"')
        values=$(op get item $uuid)
        echo $name
        echo $values | jq .overview.url| tr -d '"'
        echo $values | jq .details.fields | jq -c '.[]' - | while read j
        do
                  echo $j | jq .designation | tr -d '"'
                  echo $j | jq .value | tr -d '"'
        done
        
    fi
done
read  -n 1
