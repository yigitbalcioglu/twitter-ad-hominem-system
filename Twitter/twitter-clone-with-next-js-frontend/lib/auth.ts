import NextAuth from "next-auth"
import Google from "next-auth/providers/google"
import Credentials from "next-auth/providers/credentials"
import getWithEmail from "@/app/api/getWithEmail";
import { toast } from 'react-toastify';

function getErrorMessage(data: any): string {
    if (!data) {
        return "Kayit basarisiz oldu";
    }

    if (typeof data.detail === "string") {
        return data.detail;
    }

    if (typeof data === "object") {
        const firstKey = Object.keys(data)[0];
        const firstValue = firstKey ? data[firstKey] : null;
        if (Array.isArray(firstValue) && firstValue.length > 0) {
            return String(firstValue[0]);
        }
        if (typeof firstValue === "string") {
            return firstValue;
        }
    }

    return "Kayit basarisiz oldu";
}

export async function signup(values: any) {
    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: values.username,
                email: values.email,
                password: values.password,
            }),
        });

        if (!response.ok) {
            const data = await response.json().catch(() => null);
            throw new Error(getErrorMessage(data));
        }

        toast.success('Kayit basarili!');
    } catch (error) {
        const message = error instanceof Error ? error.message : 'Kayit basarisiz oldu';
        toast.error(message);
        throw error;
    }

    // Call the provider or db to create a user...
}

export const { handlers, signIn, signOut, auth } = NextAuth({
    providers: [Google,
        Credentials({
            // You can specify which fields should be submitted, by adding keys to the `credentials` object.
            // e.g. domain, username, password, 2FA token, etc.
            credentials: {
                email: {},
                password: {},
            },
            authorize: async (credentials) => {
                let user = null

                // logic to salt and hash password
                //const pwHash = saltAndHashPassword(credentials.password)

                // logic to verify if the user exists
                user = await getWithEmail(credentials.email)

                if (!user) {
                    // No user found, so this is their first attempt to login
                    // meaning this is also the place you could do registration
                    throw new Error("User not found.")
                }

                // return user object with their profile data
                return user
            },
        }),
    ],
})