# list safe navigation
def list_get(l, idx, default = None):
  try:
    return l[idx]
  except IndexError:
    return default