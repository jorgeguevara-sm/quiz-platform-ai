"use client";
import { useState } from "react";
import { api, OnboardingInput } from "../../lib/api";

const STEPS = ["Quien eres", "Que haces", "Objetivo"];

export default function Onboarding() {
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [form, setForm] = useState<OnboardingInput>({
    professional_name: "",
    profession: "",
    industry: "",
    business_description: "",
    test_goal: "calificar_leads",
    language: "es",
    num_questions: 8,
  });

  const update = (field: keyof OnboardingInput, value: any) =>
    setForm((prev) => ({ ...prev, [field]: value }));

  const submit = async () => {
    setLoading(true);
    try {
      const { data } = await api.post("/tests/generate", form);
      setResult(data);
    } catch (err: any) {
      alert(err?.response?.data?.detail || "Error generando el test");
    } finally {
      setLoading(false);
    }
  };

  if (result) {
    return (
      <main className="max-w-2xl mx-auto py-16 px-4">
        <h2 className="text-2xl font-bold mb-2">{result.title}</h2>
        <p className="text-slate-500 mb-6">{result.questions.length} preguntas generadas</p>
        <a href={`/editor/${result.id}`} className="bg-blue-600 text-white px-5 py-2 rounded-lg">
          Editar mi test
        </a>
      </main>
    );
  }

  return (
    <main className="max-w-xl mx-auto py-16 px-4">
      <div className="flex gap-2 mb-8">
        {STEPS.map((s, i) => (
          <div key={s} className={`flex-1 h-1 rounded ${i <= step ? "bg-blue-600" : "bg-slate-200"}`} />
        ))}
      </div>

      {step === 0 && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Quien eres?</h2>
          <input className="w-full border rounded-lg p-3" placeholder="Tu nombre"
            value={form.professional_name} onChange={(e) => update("professional_name", e.target.value)} />
          <input className="w-full border rounded-lg p-3" placeholder="Tu profesion"
            value={form.profession} onChange={(e) => update("profession", e.target.value)} />
          <input className="w-full border rounded-lg p-3" placeholder="Industria (ej: legal, salud)"
            value={form.industry} onChange={(e) => update("industry", e.target.value)} />
        </div>
      )}

      {step === 1 && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Que haces?</h2>
          <textarea className="w-full border rounded-lg p-3 h-32" placeholder="Describe tu negocio o servicio"
            value={form.business_description} onChange={(e) => update("business_description", e.target.value)} />
        </div>
      )}

      {step === 2 && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Objetivo del test</h2>
          <select className="w-full border rounded-lg p-3"
            value={form.test_goal} onChange={(e) => update("test_goal", e.target.value)}>
            <option value="calificar_leads">Calificar leads</option>
            <option value="diagnosticar_necesidades">Diagnosticar necesidades</option>
            <option value="evaluar_conocimiento">Evaluar conocimiento</option>
            <option value="recomendar_servicios">Recomendar servicios</option>
          </select>
          <label className="block text-sm text-slate-600">Numero de preguntas: {form.num_questions}</label>
          <input type="range" min={5} max={15} value={form.num_questions}
            onChange={(e) => update("num_questions", Number(e.target.value))} className="w-full" />
        </div>
      )}

      <div className="flex justify-between mt-8">
        {step > 0 ? (
          <button onClick={() => setStep(step - 1)} className="text-slate-500">Atras</button>
        ) : <span />}
        {step < STEPS.length - 1 ? (
          <button onClick={() => setStep(step + 1)} className="bg-blue-600 text-white px-5 py-2 rounded-lg">
            Siguiente
          </button>
        ) : (
          <button onClick={submit} disabled={loading} className="bg-blue-600 text-white px-5 py-2 rounded-lg disabled:opacity-50">
            {loading ? "Generando..." : "Generar test con IA"}
          </button>
        )}
      </div>
    </main>
  );
}
