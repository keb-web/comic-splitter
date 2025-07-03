import { useState } from 'react'
import './App.css'
// TODO: remove import
import testImage from './assets/lantern.JPEG';
// TODO:
// when 'reset pressed' remove


function SubmitImage({ setSplitImages }) {
	const valid_filetypes = ['image/jpeg', 'image/png', 'image/jpg']

	function handleSubmit(e) {
		e.preventDefault();
		const form = e.target;
		const formData = new FormData(form);
		if (!_valid_file_extension(formData)) {
			return
		}
		retrieveSplitImages(formData, form)
	}

	function _valid_file_extension(formData) {
		for (var pair of formData.entries()) {
			let filetype = pair[1].type
			if (valid_filetypes.includes(filetype) == false) {
				return false
			}
		}
		return true
	}
	async function retrieveSplitImages(formData, form) {
		const some_endpoint = 'http://127.0.0.1:8000/split'
		try {
			const response = await fetch(some_endpoint, {
				method: form.method,
				body: formData,
				// headers: { "Content-Type": "multipart/form-data" }
			});
			if (!response.ok) {
				throw new Error('Response status: ${response.status}');
			}
			const imageData = await response.json()
			setSplitImages(imageData)
		} catch (error) {
			console.error(error)
		}
	}

	return (
		<form method='post' onSubmit={handleSubmit}>
			<input name='files' type='file' accept='image/png, image/jpeg, image/jpg' multiple />
			<button type="reset" onClick={() => { setSplitImages([]) }}>Reset form</button>
			<button type="submit">Submit form</button>
			<hr />
		</form>
	);
}
// TODO: understand difference

//
// function ImagePreview({ splitImages }) {
// 	if (splitImages.length == 0) {
// 		return <p> upload comic file to preview pages</p>
// 	}
//
// 	console.log('s', splitImages)
// 	function formatImgSrc(image) {
// 		return `data:image/${splitImages.image_type};base64,${image.images}`;
// 	}
// 	const imageType = splitImages.image_type.split('/')[1];
//   	const previewImages = splitImages.images.map(formatImgSrc);
// 	console.log(previewImages)
//
// 	return (
// 		<div>
// 			{previewImages.map((image, index) => (
// 				<img key={index} src={image} alt={`img-${index}`} />
// 			))}
// 		</div>
// 	);
// }
function ImagePreview({ splitImages }) {
  if (!splitImages || !splitImages.images) {
    return <div>No images to preview</div>;
  }

  const imageType = splitImages.image_type.split('/')[1]; // e.g. "png"

  const previewImages = splitImages.images.map((base64) =>
    `data:image/${imageType};base64,${base64}`
  );

  return (
    <div>
      {previewImages.map((src, index) => (
        <img key={index} src={src} alt={`img-${index}`} />
      ))}
    </div>
  );
}


function App() {
	const [splitImages, setSplitImages] = useState([])

	return (
		<>
			<h1>comic splitter</h1>
			<p>only png and jpeg supported currently</p>
			<SubmitImage setSplitImages={setSplitImages} />
			<button>download as .zip</button>
			<ImagePreview splitImages={splitImages} />
		</>
	)
}

export default App
