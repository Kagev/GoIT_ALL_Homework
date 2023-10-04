from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize


def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_arhive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()), target_folder)
    except shutil.ReadError:
        folder_for_file.rmdir()
        return None
    filename.unlink()

def handle_folder(folder: Path) -> None:
    try:
        folder.rmdir()
    except OSError:
        print(f'Sorry, we can not delete the folder: {folder}')

def main(folder: Path) -> None:
    parser.scan(folder)
    for file in parser.JPEG_IMAGES:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in parser.JPG_IMAGES:
        handle_media(file, folder / 'images' / 'JPG')
    for file in parser.PNG_IMAGES:
        handle_media(file, folder / 'images' / 'PNG')
    for file in parser.SVG_IMAGES:
        handle_media(file, folder / 'images' / 'SVG')

    for file in parser.MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in parser.OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in parser.WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')
    for file in parser.AMR_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR')
    
    for file in parser.MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in parser.WAV_AUDIO:
        handle_media(file, folder / 'video' / 'WAV')
    for file in parser.AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    for file in parser.MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')

    for file in parser.DOC_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'doc')
    for file in parser.DOCX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'docx')
    for file in parser.PDF_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'pdf')
    for file in parser.PPTX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'pptx')
    for file in parser.XLSX_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'xlsx')
    for file in parser.TXT_DOCUMENTS:
        handle_media(file, folder / 'documents' / 'txt')

    
    for file in parser.ZIP_ARCHIVES:
        handle_arhive(file, folder / 'archives')
    for file in parser.TAR_ARCHIVES:
        handle_arhive(file, folder / 'archives')
    for file in parser.GZ_ARCHIVES:
        handle_arhive(file, folder / 'archives')

    for file in parser.UNKNOWN_FILES:
        handle_other(file, folder / 'UNKNOWN_FILES')

    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)


if __name__ == '__main__':
    folder_for_scan = Path(sys.argv[1])
    main(folder_for_scan.resolve())
