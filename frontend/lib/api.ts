import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({ baseURL: API_URL });

export function setAuthToken(token: string) {
  localStorage.setItem("access_token", token);
  api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

export function loadAuthToken() {
  const token = localStorage.getItem("access_token");
  if (token) api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  return token;
}

export interface OnboardingInput {
  professional_name: string;
  profession: string;
  industry: string;
  business_description: string;
  test_goal: "calificar_leads" | "diagnosticar_necesidades" | "evaluar_conocimiento" | "recomendar_servicios";
  language: "es" | "en";
  num_questions: number;
}
