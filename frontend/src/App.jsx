import { useState } from 'react'
import './App.css'


function SubmitImage({ setSplitImages }) {
	const [label, setLabel] = useState(false)
	const [blank, setBlank] = useState(false)
	const [margins, setMargins] = useState(0)
	const [mode, setMode] = useState('crop')

	const valid_filetypes = ['image/jpeg', 'image/png', 'image/jpg']

	function handleSubmit(e) {
		e.preventDefault();
		const form = e.target;
		const formData = new FormData(form);
		if (!_valid_file_extension(formData)) {
			return
		}

		formData.append("label", label);
		formData.append("blank", blank);
		formData.append("margins", margins);
		formData.append("mode", mode);

		retrieveSplitImages(formData, form)
	}

	function _valid_file_extension(formData) {
		const file = formData.get('files')
		if (valid_filetypes.includes(file.type) == false) {
			console.error('Invalid File Type')
			return false
		}
		return true
	}

	async function retrieveSplitImages(formData, form) {
		const some_endpoint = 'http://127.0.0.1:8000/split'
		try {
			const response = await fetch(some_endpoint, {
				method: form.method,
				body: formData,
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
			<div class='formSettings'>
				<label>
					<input type="radio" name="mode" value="crop" checked={mode == 'crop'} onChange={() => setMode('crop')}/>
					Crop
				</label>
				<label>
					<input type="radio" name="mode" value="etch" checked={mode == 'etch'} onChange={() => setMode('etch')}/>
					Etch
				</label>
				<label>
					<input type="checkbox" id="label" name="label" value="label" checked={label} onChange={(e) => setLabel(e.target.checked)}/>
					Label
				</label>
				<label>
					<input type="checkbox" id="blank" name="blank" value="blank" checked={blank} onChange={(e) => setBlank(e.target.checked)}/>
					Blank
				</label>
				<label>
					Margins
					<input type="number" id="margins" name="margins" min='0' max='90' value={margins} onChange={(e) => setMargins(e.target.value)}/> </label>
			</div>
			<hr />
		</form>
	);
}

function ImagePreview({ splitImages }) {
	if (!splitImages || !splitImages.images) {
		return <div>No images to preview</div>;
	}

	const imageType = splitImages.image_type.split('/')[1];
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
			<p>only png and jpeg supported currently...</p>
			<SubmitImage setSplitImages={setSplitImages} />
			<button class='zip'>download as .zip</button>
			<ImagePreview splitImages={splitImages} />
		</>
	)
}

export default App
