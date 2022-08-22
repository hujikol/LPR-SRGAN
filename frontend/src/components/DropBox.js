import React from "react";
import { useDropzone } from "react-dropzone";

function DropBox(props) {
  const { acceptedFiles, fileRejections, getRootProps, getInputProps } =
    useDropzone({
      accept: {
        "image/jpeg": [],
      },
    });

  const acceptedFileItems = acceptedFiles.map((file, index) => (
    <div>
      <li className='font-bold text-center list-none' key={file.path}>
        Uploaded File:
        <br />
        {file.path} - {file.size} bytes
      </li>
    </div>
  ));

  const fileRejectionItems = fileRejections.map(({ file, errors }) => (
    <li className='text-red-500 text-center list-none' key={file.path}>
      {file.path} - {file.size} bytes
      <ul>
        {errors.map((e) => (
          <li className='text-red-500 text-center list-none' key={e.code}>
            {e.message}
          </li>
        ))}
      </ul>
    </li>
  ));

  function DefaultLabel(props) {
    return (
      <div className='px-4 text-gray-400 text-center'>
        <p>Drag 'n' drop some files here, or click to select files</p>
        <em>Only *.jpg and *.jpeg images will be accepted</em>
      </div>
    );
  }

  function LabelText(props) {
    if (fileRejectionItems[0]) {
      return fileRejectionItems;
    }

    if (acceptedFileItems[0]) {
      return acceptedFileItems;
    }

    return <DefaultLabel />;
  }

  return (
    <div className='flex container flex-col justify-center items-center mx-auto mt-16 w-full'>
      <div className='mx-auto w-10/12 hover:bg-gray-100'>
        <div {...getRootProps({ className: "dropzone" })}>
          <label
            htmlFor='dropzone-file'
            className='flex flex-col justify-center items-center h-64
            rounded-lg border-2 border-gray-300 border-dashed cursor-pointer'
          >
            <LabelText />
            {console.log(acceptedFileItems[0])}
            <input {...getInputProps()} />
          </label>
        </div>
      </div>
      <div className='flex flex-col mt-4'>
        <button
          className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-8 rounded'
          type='submit'
        >
          Super!
        </button>
      </div>
    </div>
  );
}

export default DropBox;
