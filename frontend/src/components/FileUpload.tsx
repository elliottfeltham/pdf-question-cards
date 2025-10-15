import React from "react";
import Button from "../components/Button";
import { FileText } from "lucide-react";
import type { Question } from "../types";
import styles from "./FileUpload.module.css";

type FileUploadProps = {
	setQuestions: (questions: Question[]) => void;
	setError: (error: string | null) => void;
	setLoading: (loading: boolean) => void;
};

const FileUpload = ({
	setQuestions,
	setError,
	setLoading,
}: FileUploadProps) => {
	const fileInputRef = React.createRef<HTMLInputElement>();

	const handleUploadButton = () => {
		fileInputRef.current?.click();
	};

	const handleFileChange = async (
		event: React.ChangeEvent<HTMLInputElement>
	) => {
		setError(null);
		setLoading?.(true);

		const file = event.target.files?.[0];
		if (!file) {
			console.log("No file selected");
			return;
		}
		console.log("Selected file:", file);

		const data = new FormData();
		data.append("file", file);
		const response = await fetch("/api/generate_questions", {
			method: "POST",
			body: data,
		});

		const responseData = await response.json();

		if (responseData.error) {
			// Handle error: show message to user, log, etc.
			setLoading(false);
			setError(responseData.error);
			console.error("Error from server:", responseData.error);
			return;
		}

		console.log("Server response:", responseData);

		setLoading(false);
		setQuestions(responseData.questions);
	};

	return (
		<section className={styles.file_upload}>
			<FileText className={styles.file_icon} />
			{/* Hidden file input */}
			<input
				type="file"
				accept="application/pdf"
				ref={fileInputRef}
				style={{ display: "none" }}
				onChange={handleFileChange}
			/>
			<p>Click the button to upload a PDF file</p>
			<Button
				text="Upload PDF"
				color="green"
				onClick={handleUploadButton}
			/>
		</section>
	);
};

export default FileUpload;
