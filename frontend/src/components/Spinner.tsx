import style from "./Spinner.module.css";

const Spinner = () => {
	return (
		<div style={{ display: "inline-flex", alignItems: "center", gap: 8 }}>
			<span className={style.spin} />
			<span>Creating your questions…</span>
		</div>
	);
};

export default Spinner;
