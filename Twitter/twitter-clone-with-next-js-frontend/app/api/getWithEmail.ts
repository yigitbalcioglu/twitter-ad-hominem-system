export default async function getWithEmail(email: unknown) {
    try {

        // Örneğin, Strapi API'ye POST isteği:
        const response = await fetch(`http://localhost:1337/api/all-users?filters[email][$eq]=${email}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        const data = await response.json();

        if (!data || data.data.length === 0) {
            throw new Error('Kullanıcı bulunamadı.');
        }

        const user = data.data[0].attributes;
        return user

    } catch (error) {
        throw (error)
    }
}