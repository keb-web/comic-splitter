function ImagePreview({ splitData }) {
	if (!splitData || !splitData.images) {
		return <div></div>;
	}

	const imageType = splitData.image_type.split('/')[1];
	const previewImages = splitData.images.map((base64) =>
		`data:image/${imageType};base64,${base64}`
	);

	return (
		<>
			<div>
				{previewImages.map((src, index) => (
					<img key={index} src={src} alt={`img-${index}`} />
				))}
			</div>
		</>
	);
}


export default ImagePreview
