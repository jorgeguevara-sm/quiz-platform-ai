"use client";
import { useEffect, useState } from "react";
import { api } from "../../../lib/api";

export default function PublicQuiz({ params }: { params: { slug: string } }) {
  const [test, setTest] = useState<any>(null);
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [current, setCurrent] = useState(0);
  const [submitted, setSubmitted] = useState<any>(null);
  const [contact, setContact] = useState({ respondent_name: "", respondent_email: "", respondent_phone: "" });

  useEffect(() => {
    api.get(`/public/tests/${params.slug}`).then(({ data }) => setTest(data));
  }, [params.slug]);

  if (!test) return <p className="text-center py-16">Cargando...</p>;

  const question = test.questions[current];
  const isLast = current === test.questions.length - 1;

  const answer = (value: any) => {
    setAnswers((prev) => ({ ...prev, [question.id]: value }));
    if (!isLast) setCurrent(current + 1);
  };

  const submit = async () => {
    const { data } = await api.post(`/public/tests/${params.slug}/responses`, {
      ...contact,
      answers,
    });
    setSubmitted(data);
  };

  if (submitted) {
    const result = test.results.find((r: any) => r.label === submitted.result_label);
    return (
      <main className="max-w-lg mx-auto py-20 px-4 text-center">
        <h2 className="text-2xl font-bold mb-4">{submitted.result_label}</h2>
        <p className="text-slate-600 mb-6">{result?.message}</p>
        {result?.cta_text && (
          <button className="bg-blue-600 text-white px-6 py-3 rounded-lg">{result.cta_text}</button>
        )}
      </main>
    );
  }

  return (
    <main
      className="max-w-lg mx-auto py-16 px-4"
      style={{ borderTop: `4px solid ${test.branding?.primary_color || "#2563eb"}` }}
    >
      <p className="text-sm text-slate-400 mb-2">Pregunta {current + 1} de {test.questions.length}</p>
      <h2 className="text-xl font-semibold mb-6">{question.text}</h2>

      {question.type === "multiple_choice" || question.type === "yes_no" ? (
        <div className="space-y-3">
          {question.options.map((opt: any) => (
            <button key={opt.value} onClick={() => answer(opt.value)}
              className="w-full text-left border rounded-lg p-3 hover:bg-blue-50">
              {opt.label}
            </button>
          ))}
        </div>
      ) : question.type === "scale" ? (
        <div className="flex gap-3 justify-center">
          {[1, 2, 3, 4, 5].map((n) => (
            <button key={n} onClick={() => answer(n)} className="w-12 h-12 border rounded-full hover:bg-blue-50">
              {n}
            </button>
          ))}
        </div>
      ) : (
        <textarea className="w-full border rounded-lg p-3 h-24" onBlur={(e) => answer(e.target.value)} />
      )}

      {isLast && Object.keys(answers).length === test.questions.length && (
        <div className="mt-8 space-y-3">
          <input className="w-full border rounded-lg p-3" placeholder="Tu nombre"
            onChange={(e) => setContact({ ...contact, respondent_name: e.target.value })} />
          <input className="w-full border rounded-lg p-3" placeholder="Tu email"
            onChange={(e) => setContact({ ...contact, respondent_email: e.target.value })} />
          <button onClick={submit} className="bg-blue-600 text-white px-6 py-3 rounded-lg w-full">
            Ver mi resultado
          </button>
        </div>
      )}
    </main>
  );
}
