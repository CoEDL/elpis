
export const getFileExtension = (filename) => {
    filename = filename.slice((filename.lastIndexOf(".") - 1 >>> 0) + 2);
    return filename;
};
