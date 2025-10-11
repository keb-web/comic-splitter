import { useState } from 'react'

import ImagePreview from './ImagePreview'
import ImageSubmit from './ImageSubmit'
import './App.css'
import CanvasPreview from './CanvasPreview'

function App() {
	const [splitImages, setSplitImages] = useState([])
	const [splitTemplate, setSplitTemplate] = useState([])
	const [splitData, setSplitData] = useState([])

	return (
		<div class='app'>
			<div class='header'>
				<h1>comic splitter</h1>
			</div>

			<div class='options'>
				<ImageSubmit setSplitImages={setSplitImages} setSplitTemplate={setSplitTemplate} setSplitData={setSplitData}/>
				<button class='zip'>download as .zip</button>
			</div>

			<div class='imageGallery'>
				<CanvasPreview splitTemplate={splitTemplate} splitImages={splitImages}/>
				<ImagePreview splitData={splitData} />
			</div>
		</div>
	)
}

export default App
