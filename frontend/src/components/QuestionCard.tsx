type Props = {
	question: string;
};

const QuestionCard = ({ question }: Props) => {
	return <div>{question}</div>;
};

export default QuestionCard;
