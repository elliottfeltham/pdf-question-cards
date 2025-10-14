import styles from "./Button.module.css";

type ButtonProps = {
	text: string;
	color: "primary" | "secondary";
	handleClick: () => void;
};

const Button = ({ text, color, handleClick }: ButtonProps) => {
	return (
		<button
			className={`${styles.button} ${styles[color]}`}
			onClick={handleClick}
		>
			{text}
		</button>
	);
};

export default Button;
