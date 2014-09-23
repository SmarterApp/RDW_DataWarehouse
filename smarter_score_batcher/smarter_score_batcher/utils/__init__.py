

def get_sub_settings_by_prefix(settings, prefix, delete_prefix):
    return {(k[len(prefix) + 1:] if delete_prefix else k, v) for (k, v) in settings.items if k.startswith(prefix)}
