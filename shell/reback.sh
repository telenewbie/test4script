#!/bin/bash
FileListArrays=()
DirListArrays=()


function read_dir()
{
    for file in `ls  $1`
    do
        if [ -d $1"/"$file ]
        then
            if [ -L $1"/"$file"." ]
            then
                SoftLinkList+=$1"/"$file
            elif [ $file == "android" ]
            then
                echo "hahahahahahahha"
            else
                read_dir $1"/"$file
            fi
        else
            FileListArrays+=($file)
            DirListArrays+=($1)
            FileList+=$file" " #空格分割
            FileDirList+=$1" "
        fi
    done
}

MyFileListArrays=()
MyDirListArrays=()
function read_myself()
{
    for file in `ls  $1`
    do
        if [ -d $1"/"$file ]
        then
            if [ -L $1"/"$file"." ]
            then
                SoftLinkList+=$1"/"$file
            else
                read_myself $1"/"$file
            fi
        else
            MyFileListArrays+=($file)
            MyDirListArrays+=($1)
        fi
    done
}


echo $1
echo $2
read_dir $1
read_myself $2

count=0
compare=0 #对比的次数
testMax=3000 #最大对比次数
for file in ${FileListArrays[@]}
do
#    echo $file
    # 如果存在在这里面
    compare=0
    for item in ${MyFileListArrays[@]}
    do
        if [ $item == $file ]
        then
            #echo "this is same "$file":::"$item
            echo cp ${MyDirListArrays[$compare]}/${MyFileListArrays[$compare]}  ${DirListArrays[$count]}/${FileListArrays[$count]}
#            echo ${DirListArrays[$count]}/${FileListArrays[$count]}
            #cp ${MyDirListArrays[$compare]}/${MyFileListArrays[$compare]}  ${DirListArrays[$count]}/${FileListArrays[$count]}
        fi
        compare=`expr $compare + 1`
    done

    count=`expr $count + 1`
    if [ $count -ge $testMax ]
    then
        break
    fi
done
echo $count
#i=0
#for file in $FileDirList
#do
#    i+=1
#    #echo $file
#done
#echo "一共有"$i" 个选项"
#a=0
#for file in $FileList
#do
#    a+=1
#done
#echo "一共有"$a" 个选项"




