from pydoc import locate

def get_class_by_name(class_path):
    cls = locate(class_path)
    return cls
