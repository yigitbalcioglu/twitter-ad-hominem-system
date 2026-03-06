import { NextRequest, NextResponse } from "next/server";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";
const protectedRoutes = ["/home"];
const publicRoutes = ["/login", "/register", "/"];

export async function middleware(req: NextRequest) {
  const path = req.nextUrl.pathname;
  const isProtectedRoute = protectedRoutes.includes(path);
  const isPublicRoute = publicRoutes.includes(path);

  let accessToken = req.cookies.get("accessToken")?.value;
  const refreshToken = req.cookies.get("refreshToken")?.value;
  const secureCookie = process.env.NODE_ENV === "production";

  let response = NextResponse.next();

  if (!accessToken && refreshToken) {
    const refreshResponse = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (refreshResponse.ok) {
      const data = await refreshResponse.json();
      accessToken = data.access;
      response.cookies.set("accessToken", data.access, {
        httpOnly: true,
        secure: secureCookie,
        sameSite: "lax",
        path: "/",
      });
    }
  }

  if (isProtectedRoute && !accessToken) {
    const loginUrl = new URL("/login", req.nextUrl);
    loginUrl.searchParams.set("redirect", path);
    const redirectResponse = NextResponse.redirect(loginUrl);
    redirectResponse.cookies.delete("accessToken");
    redirectResponse.cookies.delete("refreshToken");
    return redirectResponse;
  }

  if (path === "/" && accessToken) {
    return NextResponse.redirect(new URL("/home", req.nextUrl));
  }

  return response;
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|.*\\.png$).*)"],
};
