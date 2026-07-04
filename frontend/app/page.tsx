export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-blue-50 to-white px-4">
      <h1 className="text-4xl font-bold text-slate-800 mb-4">
        Crea tests inteligentes con IA
      </h1>
      <p className="text-slate-600 mb-8 max-w-md text-center">
        Describe tu negocio y genera un cuestionario completo en segundos.
        Sin disenadores, sin desarrolladores.
      </p>
      <a
        href="/onboarding"
        className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition"
      >
        Crear mi primer test gratis
      </a>
    </main>
  );
}
