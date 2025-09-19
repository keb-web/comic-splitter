import { useState } from 'react'

import ImagePreview from './ImagePreview'
import ImageSubmit from './ImageSubmit'
import './App.css'

function App() {
	const [splitImages, setSplitImages] = useState([])

	return (
		<>
			<h1>comic splitter</h1>
			<p>only png and jpeg supported currently...</p>
			<ImageSubmit setSplitImages={setSplitImages} />
			<button class='zip'>download as .zip</button>
			<ImagePreview splitImages={splitImages} />
		</>
	)
}

export default App
