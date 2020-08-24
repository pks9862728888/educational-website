import { STUDY_MATERIAL_CONTENT_TYPE_REVERSE } from '../../constants';

export function getFileSize(fileSize: number) {
    if (fileSize >= 1000000000) {
      return (fileSize / 1000000000).toFixed(3) + ' GB';
    } else if (fileSize >= 1000000) {
      return (fileSize / 1000000).toFixed(3) + ' MB';
    } else if (fileSize >= 1000) {
      return (fileSize / 1000).toFixed(3) + ' KB';
    } else {
      return fileSize + ' bytes';
    }
  }

export function isContentTypeImage(key: string) {
  if (key === STUDY_MATERIAL_CONTENT_TYPE_REVERSE['IMAGE']) {
    return true;
  } else {
    return false
  }
}

export function isContentTypeVideo(key: string) {
  if (key === STUDY_MATERIAL_CONTENT_TYPE_REVERSE['VIDEO']) {
    return true;
  } else {
    return false
  }
}

export function isContentTypeExternalLink(key: string) {
  if (key === STUDY_MATERIAL_CONTENT_TYPE_REVERSE['EXTERNAL_LINK']) {
    return true;
  } else {
    return false
  }
}

export function isContentTypePdf(key: string) {
  if (key === STUDY_MATERIAL_CONTENT_TYPE_REVERSE['PDF']) {
    return true;
  } else {
    return false
  }
}
