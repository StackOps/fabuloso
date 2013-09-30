Key Pairs
=========

*FABuloso* can manage **keypairs** in order to securely connect to the target hosts and execute *services*. *Keypairs* will be referenced later when :ref:`adding environments <adding_environment>`.


Listing keypairs
----------------

By default *FABuloso* comes with the *nonsecure* keypair. You can list keypairs to see it::

    fabuloso > list_keys
     * nonsecure
    fabuloso >


Showing a keypair
-----------------

Also you can get the key info and contents by running::

    fabuloso > show_key nonsecure
     * Name: nonsecure
     * Key file: /etc/fabuloso/keys/nonsecureid_rsa
     * Key: -----BEGIN RSA PRIVATE KEY-----
    MIIEowIBAAKCAQEAtO4zZwNYOzux [...]
    -----END RSA PRIVATE KEY-----

     * Pub file: /etc/fabuloso/keys/nonsecureid_rsa.pub
     * Pub: ssh-rsa AAAAB3Nza [...] contactus@stackops.com


.. _adding_keypair:

Adding a keypair
----------------

To add a new *keypair* run::

    fabuloso > add_key
    -(Adding new keypair)-Name: my-secure-key
    -(Adding new keypair)-Key path: ~/my-secure-key
    -(Adding new keypair)-Pub path: ~/my-secure-key.pub
    fabuloso >

Now list the keys to see the new added key::

    fabuloso > list_keys
     * nonsecure
     * my-secure-key
    fabuloso >


Removing a keypair
------------------

.. warning::

    The *del_key* command is not implemented yet.
