EDWARE = EDWARE or {}

#
# * Description: This function creates namespaces under EDWARE.
# * @param ns_string - namespace string
# * @param assignee - the function which can be assigned to the namespace
# * @return parent object
# * Example: EDWARE.namespace('EDWARE.modules.module1');
# 
EDWARE.namespace = (ns_string, assignee) ->
  parts = ns_string.split(".")
  parent = EDWARE
  i = undefined
  parts = parts.slice(1)  if parts[0] is "EDWARE"
  i = 0
  while i < parts.length
    if typeof parent[parts[i]] is "undefined"
      parent[parts[i]] = {}
      parent[parts[i]] = assignee  if assignee and i is parts.length - 1
    parent = parent[parts[i]]
    i += 1
  parent