export default function Hints({ hints }) {
    return (
        <div className="hints-container">
            {hints.map((hint, index) => (
                <p key={index}>{hint}</p>
            ))}
        </div>
    )
}