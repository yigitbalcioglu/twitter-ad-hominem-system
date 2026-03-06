import { NextRequest, NextResponse } from 'next/server';

export async function GET(req: NextRequest) {

    const { userId } = await req.json();

    try {
        const response = await fetch(`http://localhost:1337/api/posts?sort=createdAt:desc&filters[parent][${userId}]=true`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        const data = await response.json();
        return NextResponse.json(data);

    }
    catch (error) {
        return Response.json({ message: "Internal Error" }, { status: 500 })
    }
}