import React from "react";
import type { Question } from "../types";
import style from "./QuestionCard.module.css";
import Button from "./Button";

type Props = {
	question: Question;
	color: string;
	questionNumber?: number;
};

const QuestionCard = ({ question, color, questionNumber }: Props) => {
	const [showSolution, setShowSolution] = React.useState(false);

	const toggleSolution = () => {
		setShowSolution(!showSolution);
	};

	return (
		<div className={`${style.card} ${style[color]}`}>
			<div className={style.header}>
				<h3>Question {questionNumber}:</h3>
				<h2
					className={
						question.type == "coding" ? style.coding : style.theory
					}
				>
					{question.type}
				</h2>
			</div>
			<p>{question.prompt_md}</p>

			<textarea
				className={style.codeArea}
				placeholder="Write your answer here..."
			></textarea>
			{/* Button to toggle solution */}
			<Button
				onClick={toggleSolution}
				text={showSolution ? "Hide Solution" : "Show Solution"}
				color="green"
			/>
			{showSolution && question.solution_md && (
				<>
					<h3>Solution:</h3>
					<p>{question.solution_md}</p>
				</>
			)}
			{showSolution && question.solution_code && (
				<>
					<h3>Solution code:</h3>
					<p>{question.solution_code}</p>
				</>
			)}
		</div>
	);
};

export default QuestionCard;
