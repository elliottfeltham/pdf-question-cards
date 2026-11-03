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

type GenerateQuestionsResponse = {
	questions?: Question[];
	error?: string;
	detail?: string;
};

const MAX_PDF_BYTES = 10 * 1024 * 1024;

const FileUpload = ({
	setQuestions,
	setError,
	setLoading,
}: FileUploadProps) => {
	const fileInputRef = React.useRef<HTMLInputElement>(null);

	const handleUploadButton = () => {
		fileInputRef.current?.click();
	};

	const handleFileChange = async (
		event: React.ChangeEvent<HTMLInputElement>
	) => {
		setError(null);

		const file = event.target.files?.[0];
		if (!file) return;
		if (file.type !== "application/pdf") {
			setError("Please select a PDF file.");
			event.target.value = "";
			return;
		}
		if (file.size > MAX_PDF_BYTES) {
			setError("PDF exceeds the 10 MB upload limit.");
			event.target.value = "";
			return;
		}

		setLoading(true);
		try {
			const data = new FormData();
			data.append("file", file);
			const response = await fetch("/api/generate_questions", {
				method: "POST",
				body: data,
			});
			const responseData = (await response.json()) as GenerateQuestionsResponse;

			if (!response.ok || responseData.error || !responseData.questions) {
				throw new Error(
					responseData.detail ||
						responseData.error ||
						"Question generation failed. Please try again."
				);
			}
			setQuestions(responseData.questions);
		} catch (error) {
			setError(
				error instanceof Error
					? error.message
					: "Question generation failed. Please try again."
			);
		} finally {
			setLoading(false);
			event.target.value = "";
		}
	};

	return (
		<section className={styles.file_upload}>
			<FileText className={styles.file_icon} />
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
