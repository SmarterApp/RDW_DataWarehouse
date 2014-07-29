import os


def generate_file_path(items_root_dir, extension, state_code=None, asmt_year=None,
                       asmt_type=None, effective_date=None, asmt_subject=None,
                       asmt_grade=None, district_id=None, student_id=None, **kwargs):
    """Generates a directory path or a file path with file extension.

    Return value has below format:

    items_root_dir/<state_code>/<asmt_year>/<asmt_type>/[effective_date]/<asmt_subject>/<asmt_grade>/<district_id>/<student_id>.extension

    A whole file path is generated if all named parameters except
    effective_date have a not None value. If effective_date is None,
    this function will skip it and continue generating path for the
    rest, whereas if any other parameters have a value of None, this
    function will return currently generated path immediately, which
    is a path to a directory.

    """
    if type(asmt_year) is int:
        asmt_year = str(asmt_year)
    if type(effective_date) is int:
        effective_date = str(effective_date)
    if type(asmt_grade) is int:
        asmt_grade = str(asmt_grade)
    path = items_root_dir
    if state_code is not None:
        path = os.path.join(path, state_code)
    else:
        return path
    if asmt_year is not None:
        path = os.path.join(path, asmt_year)
    else:
        return path
    if asmt_type is not None:
        path = os.path.join(path, asmt_type.upper().replace(' ', '_'))
    else:
        return path
    if effective_date is not None:
        path = os.path.join(path, effective_date)
    if asmt_subject is not None:
        path = os.path.join(path, asmt_subject.upper())
    else:
        return path
    if asmt_grade is not None:
        path = os.path.join(path, asmt_grade)
    else:
        return path
    if district_id is not None:
        path = os.path.join(path, district_id)
    else:
        return path
    if student_id is not None:
        path = os.path.join(path, student_id + "." + extension)
    return path
