// import { Stage, Layer, Rect, Circle } from 'react-konva';
// import ImageGallery from "react-image-gallery";


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

// function ImagePreview({ splitImages }) {
// 	if (!splitImages || !splitImages.images) {
// 		return <div>No images to preview</div>;
// 	}
//
// 	const imageType = splitImages.image_type.split('/')[1];
// 	const previewImages = splitImages.images.map((base64) =>
// 		`data:image/${imageType};base64,${base64}`
// 	);
// 	const galleryItems = previewImages.map((src) => ({
// 		original: src,
// 		thumbnail: src,
// 	  }));
//
// 	return (
// 		<ImageGallery items={galleryItems}/>
// 	);
// }

export default ImagePreview
