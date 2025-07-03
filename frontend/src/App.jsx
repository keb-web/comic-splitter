// import { useState } from 'react'
import './App.css'

const valid_filetypes = ['image/jpeg', 'image/png', 'image/jpg']


function SubmitImage({setImage}) {

	function handleSubmit(e) {
		e.preventDefault();
		const form = e.target;
		const formData = new FormData(form);

		if (!_valid_file_extension(formData)) {
			return
		}
		splitImages = retrieveSplitImages()
		// const formJson = Object.fromEntries(formData.entries());
		// console.log('formJson', formJson)

		// TODO: `setImage` state set split image here! 
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
	async function retrieveSplitImages() {
		const some_endpoint = 'http://127.0.0.1:8000/split'
		try {
			console.log('attempting api call')
			const response = await fetch(some_endpoint, {
				method: form.method,
				body: formData,
				// headers: { "Content-Type": "multipart/form-data" }
			});
			if (!response.ok) {
				throw new Error('Response status: ${response.status}');
			}
			console.log(response.json())
			console.log('we good gang, response from fastapi encountered')
			return response.json()
		} catch (error) {
			console.error(error.messsage)
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

function ImagePreview({images}) {
	const display = () => {
	}
	return '<>'
}

function App() {
	const [hasSplitImages, setSplitImages] = useState()
	return (
		<>
			<h1>comic splitter</h1>
			<p>only png and jpeg supported currently</p>
			<SubmitImage />
			<ImagePreview/>
		</>
	)
}

export default App
