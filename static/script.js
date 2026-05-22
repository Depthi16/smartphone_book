let contacts = [];

async function fetchContacts() {

    const response =
    await fetch('/contacts');

    contacts =
    await response.json();

    displayContacts(contacts);
}

function displayContacts(data) {

    const contactsDiv =
    document.getElementById('contacts');

    contactsDiv.innerHTML = '';

    data.forEach(contact => {

        contactsDiv.innerHTML += `

        <div class="contact">

            <h3>${contact.name}</h3>

            <p>
            <strong>📞 Phone:</strong>
            ${contact.phone}
            </p>

            <p>
            <strong>📧 Email:</strong>
            ${contact.email}
            </p>

            <p>
            <strong>🏢 Company:</strong>
            ${contact.company}
            </p>

            <p>
            <strong>📍 Address:</strong>
            ${contact.address}
            </p>

            <p>
            <strong>🏷 Category:</strong>
            ${contact.category}
            </p>

            <button
            class="delete-btn"
            onclick="deleteContact(${contact.id})">

            Delete

            </button>

        </div>
        `;
    });
}

async function addContact() {

    const contact = {

        name:
        document.getElementById('name').value,

        phone:
        document.getElementById('phone').value,

        email:
        document.getElementById('email').value,

        company:
        document.getElementById('company').value,

        address:
        document.getElementById('address').value,

        category:
        document.getElementById('category').value
    };

    const response = await fetch('/add', {

        method:'POST',

        headers:{
            'Content-Type':'application/json'
        },

        body:JSON.stringify(contact)
    });

    const result =
    await response.json();

    alert(result.message);

    fetchContacts();

    document.getElementById('name').value='';
    document.getElementById('phone').value='';
    document.getElementById('email').value='';
    document.getElementById('company').value='';
    document.getElementById('address').value='';
    document.getElementById('category').value='';
}

async function deleteContact(id) {

    await fetch(`/delete/${id}`, {

        method:'DELETE'
    });

    alert('Contact Deleted');

    fetchContacts();
}

document.getElementById('search')
.addEventListener('keyup', async function(){

    const keyword = this.value;

    const response =
    await fetch(`/search?keyword=${keyword}`);

    const data =
    await response.json();

    displayContacts(data);
});

document.getElementById('sort')
.addEventListener('change', function(){

    let sorted = [...contacts];

    if(this.value === 'asc'){

        sorted.sort((a,b)=>
        a.name.localeCompare(b.name));
    }

    else if(this.value === 'desc'){

        sorted.sort((a,b)=>
        b.name.localeCompare(a.name));
    }

    displayContacts(sorted);
});

fetchContacts();