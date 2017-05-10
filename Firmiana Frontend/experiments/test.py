from authority_trans import SecurityHelper

cookie = '3ea0fcfc6f6dc403d90f8e504e6b6904ed193d6cc31dad9528890c2a2d6f15dd40c31bb552fcecda'
session = SecurityHelper().decode_guid(cookie)
print session
