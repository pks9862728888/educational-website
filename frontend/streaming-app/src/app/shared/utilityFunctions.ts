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
