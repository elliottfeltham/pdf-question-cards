import type { Question } from "../types";

type Props = {
	question: Question;
};

const QuestionCard = ({ question }: Props) => {
	return <div>{question.prompt_md}</div>;
};

export default QuestionCard;
