#!/bin/bash

# welcome
toilet -f big --gay "AutoNmap"
echo -e "\n@Author: Ly4hm\n@Usage: autonmap -t <ip> [-o <output dir>]\n"

# loading string
function loading() {
    printf "$1……  "
    symbols=("/" "-" "\\" "|")
    while true; do
        for symbol in "${symbols[@]}"; do
            printf "%s" "$symbol"
            sleep 0.1
            printf "\b"
        done
    done
}

# end loading string
function loadcomplete() {
    kill $1
    printf "\b\n"
}

# 伪闭包，在操作执行前后进行 loading string 输出
# args: 状态， 执行的操作
function dosomething() {
    loading $1 &
    loadingstring=$!

    eval $2 &
    wait $!

    loadcomplete $loadingstring
}

# 带颜色的输出
color_echo() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}


# basic args
ip=""
outputdir="nmapscan"

# 定义颜色代码
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# 解析参数
while getopts ":t:o:" opt; do
    case ${opt} in
        t)
            ip=$OPTARG
            ;;
        o)
            outputdir=$OPTARG
            ;;
        \?)
            color_echo $RED "Invalid option: $OPTARG" 1>&2
            exit 1
            ;;
    esac
done
shift $((OPTIND - 1))

# 检查当前用户是否是root用户
if [ ! $UID -eq 0 ]; then
    color_echo $RED "需要 root 权限"
    exit 1
fi

# 检查IP地址是否为空
if [ -z "$ip" ]; then
    color_echo $RED "Please check Usage!"
    exit 1
fi

# 判断连通性
loading "检查IP有效性" &
ping -c 1 -w 3 -s 1 $ip > /dev/null && reachable_flag=0 || reachable_flag=1
printf "\b"
kill $!

if [ "$reachable_flag" == 1 ]; then
    color_echo $RED "\n[-] $ip 连接失败"
    exit 1
else
    color_echo $GREEN "\n[*] $ip 连接成功"
fi

# 检查输出文件夹是否存在
if [ ! -d "./$outputdir" ]; then
    color_echo $YELLOW "[+] 输出路径不存在，将自动创建"
    mkdir $outputdir
    chmod 777 $outputdir
fi

# tcp端口扫描
order1="nmap -sT --min-rate 10000 -p- $ip -oN ${outputdir}/ports > /dev/null"
if [ ! -f "${outputdir}/ports" ]; then
    dosomething "扫描端口" "$order1"
    color_echo $GREEN "[*] 端口扫描完成"
else
    color_echo $YELLOW "[+] 读取本地 ports 结果"
fi

# 提取端口
ports=$(cat ${outputdir}/ports | grep open | awk -F'/' '{print $1}' | paste -sd ',')

# 探测版本
order2="nmap -sT -sV -sC -O -p${ports} $ip -oN ${outputdir}/detail > /dev/null"
if [ ! -f "${outputdir}/detail" ]; then
    dosomething "探测版本" "$order2"
    color_echo $GREEN "[*] 版本探测完成"
else
    color_echo $YELLOW "[+] 本地 detail 存在，跳过扫描"
fi

# 默认漏洞脚本扫描
order3="nmap --script=vuln -p${ports} $ip -oN ${outputdir}/vuln > /dev/null"
if [ ! -f "${outputdir}/vuln" ]; then
    dosomething "默认漏洞扫描" "$order3"
    color_echo $GREEN "[*] 漏洞扫描完成"
else
    color_echo $YELLOW "[+] 本地 vuln 存在，跳过扫描"
fi

color_echo $GREEN "[*] 扫描完成"
