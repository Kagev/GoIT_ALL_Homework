if not ext:
    MY_OTHER.append(full_name)
else:
    try:
        cotainer = REGISTER_EXTENSION[ext]
        EXTENSION.add(ext)
        cotainer.append(full_name)
    except KeyError:
        UNKNOWN.add(ext)
        MY_OTHER.append(full_name)
Перетворити
if ext:
    container = REGISTER_EXTENSION.get(ext)
if container is not None:
    EXTENSIONS.add(ext)
    container.append(full_name)
else:
    UNKNOWN.add(ext)
    MY_OTHER.append(full_name)
else:
    MY_OTHER.append(full_name)