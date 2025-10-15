import QuestionCard from "./QuestionCard";
import type { Question } from "../types";

type CardContainerProps = {
	questions: Question[];
};
const CardContainer = ({ questions }: CardContainerProps) => {
	return (
		<div className="card-container">
			{questions.map((question, index) => {
				return <QuestionCard key={index} question={question} />;
			})}
		</div>
	);
};

export default CardContainer;
