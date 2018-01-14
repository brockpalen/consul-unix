#!/bin/bash

#arcusers/users/<uniquename>/
#                           /common/commonName  :  Display Name
#                           /common/uid         :  unix uid
#                           /<service>/gid      :  default groupid
#                           /<service>/homedir  :  value of $HOME
#                           /<service>/shell    :  Shell for user eg /bin/bash

SERVICE=$1
UNIQUENAME=$2
USERUID=$3
USERGID=$4
CNAME=$5
USERSHELL="/bin/bash"
HOMEDIR="/home/$UNIQUENAME"

consul kv put arcusers/users/$UNIQUENAME/common/commonName "$CNAME"
consul kv put arcusers/users/$UNIQUENAME/common/uid $USERUID
consul kv put arcusers/users/$UNIQUENAME/$SERVICE/gid $USERGID
consul kv put arcusers/users/$UNIQUENAME/$SERVICE/homedir $HOMEDIR
consul kv put arcusers/users/$UNIQUENAME/$SERVICE/shell $USERSHELL
