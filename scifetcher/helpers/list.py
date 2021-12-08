# list safe navigation
def list_get(lis, idx, default = None):
  if not lis:
    return default
  try:
    return lis[idx]
  except IndexError:
    return default