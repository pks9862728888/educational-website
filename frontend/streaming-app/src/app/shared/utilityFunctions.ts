import { SUBJECT_INTRODUCTION_CONTENT_TYPE_REVERSE, LANGUAGE, COUNTRY, GENDER } from '../../constants';

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
  if (key === SUBJECT_INTRODUCTION_CONTENT_TYPE_REVERSE['IMAGE']) {
    return true;
  } else {
    return false
  }
}

export function isContentTypeVideo(key: string) {
  if (key === SUBJECT_INTRODUCTION_CONTENT_TYPE_REVERSE['VIDEO']) {
    return true;
  } else {
    return false
  }
}

export function isContentTypeLink(key: string) {
  if (key === SUBJECT_INTRODUCTION_CONTENT_TYPE_REVERSE['LINK']) {
    return true;
  } else {
    return false
  }
}

export function isContentTypePdf(key: string) {
  if (key === SUBJECT_INTRODUCTION_CONTENT_TYPE_REVERSE['PDF']) {
    return true;
  } else {
    return false
  }
}

export function getLanguage(key: any) {
  if (key) {
    return LANGUAGE[key];
  } else {
    return 'None';
  }
}

export function getCountry(key: any) {
  if (key) {
    return COUNTRY[key];
  } else {
    return 'None';
  }
}

export function getGender(key: any) {
  if (key) {
    return GENDER[key];
  } else {
    return 'None';
  }
}

export function getTimeElapsed(createdOn: string, currentTime: string) {
  const createdDate: Date = new Date(createdOn);
  const now: Date = new Date(currentTime);
  let timeInMillis = +now - +createdDate;
  let elapsedTime = '';
  let year = 0;
  let month = 0;
  let day = 0;
  let hour = 0;
  let minute = 0;
  let second = 0;
  if (timeInMillis >= 365 * 24 * 60 * 60 * 1000) {
    year = Math.round(timeInMillis / (365 * 24 * 60 * 60 * 1000));
    timeInMillis = timeInMillis % (365 * 24 * 60 * 60 * 1000);
  }
  if (timeInMillis >= 30 * 24 * 60 * 60 * 1000) {
    month = Math.round(timeInMillis / (30 * 24 * 60 * 60 * 1000));
    timeInMillis = timeInMillis % (30 * 24 * 60 * 60 * 1000);
  }
  if (timeInMillis >= 24 * 60 * 60 * 1000) {
    day = Math.round(timeInMillis / (24 * 60 * 60 * 1000));
    timeInMillis = timeInMillis % (24 * 60 * 60 * 1000);
  }
  if (timeInMillis >= 60 * 60 * 1000) {
    hour = Math.round(timeInMillis / (60 * 60 * 1000));
    timeInMillis = timeInMillis % (60 * 60 * 1000);
  }
  if (timeInMillis >= 60 * 1000) {
    minute += Math.round(timeInMillis / (60 * 1000));
    timeInMillis = timeInMillis % (60 * 1000);
  } else if (timeInMillis >= 0) {
    second = Math.round(timeInMillis / 1000);
    timeInMillis = timeInMillis % 1000;
  }
  if (year > 0) {
    elapsedTime += year + ' year ';
    if (month > 0) {
      elapsedTime += month + ' months ';
    }
    if (day > 0) {
      elapsedTime += day + ' day ';
    }
  } else if (month > 0) {
    elapsedTime += month + ' month ';
    if (day > 0) {
      elapsedTime += day + ' days ';
    }
  } else if (day > 0) {
    elapsedTime += day + ' day ';
    if (hour > 0) {
      elapsedTime += hour + ' hour ';
    }
  } else if (hour > 0) {
    elapsedTime += hour + ' hour ';
    if (minute > 0) {
      elapsedTime += minute + ' minutes ';
    }
  } else if (minute > 0) {
    elapsedTime += minute + ' minutes ';
  } else if (second > 0) {
    elapsedTime += second + ' seconds ';
  }

  if (!elapsedTime) {
    return '0 seconds ';
  }
  return elapsedTime;
}
