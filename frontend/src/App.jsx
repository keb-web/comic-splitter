import { useState } from 'react'
import './App.css'
// TODO: remove import
import testImage from './assets/lantern.JPEG';


function SubmitImage({setSplitImages}) {
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
			const imageData = response.json()
			setSplitImages(imageData)
		} catch (error) {
			console.error(error)
		}
	}

	return (
		<form method='post' onSubmit={handleSubmit}>
			<input name='files' type='file' accept='image/png, image/jpeg, image/jpg' multiple />
			<button type="reset">Reset form</button>
			<button type="submit">Submit form</button>
			<hr />
		</form>
	);
}

function ImagePreview({splitImages}) {
	if (splitImages.length == 0){
		return <p> upload comic file to preview pages</p>
	}
	return (
		<>
			<div><img src={testImage} alt='test image' ></img></div>
			<div><img src={splitImages} alt='api image' ></img></div>
		</>
	)
}

function App() {
	const [splitImages, setSplitImages] = useState([])

	return (
		<>
			<h1>comic splitter</h1>
			<p>only png and jpeg supported currently</p>
			<SubmitImage  setSplitImages={setSplitImages}/>
			<ImagePreview splitImages={splitImages}/>
		</>
	)
}

export default App
