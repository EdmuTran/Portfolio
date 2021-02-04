/**
 * This Class is meant to store creature functions
 * It should not be calling the functions with Update
 * 
 */

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Creature : MonoBehaviour
{
    private SpriteRenderer spriteRenderer;
    public Rigidbody2D rb;
    private Brain brain;

    public bool active = true;
    public int birthCountdown;
    public int birthDelay;

    public int strength;
    public int maxDisplayedStrength = 20;
    public Color minStrength;
    public Color maxStrength;

    public bool dying; // Set the creatures state to dying so that it can be removed next frame. Helps avoid bugs

    public float maxEnergy;
    [SerializeField]
    private float energy;
    public float getEnergy()
    {
        return energy;
    }
    public void setEnergy(float value)
    {
        energy = Mathf.Min(value, maxEnergy);
    }
    public void addEnergy(float value)
    {
        energy = Mathf.Min(energy + value, maxEnergy);
    }
    public void removeEnergy(float value)
    {
        energy -= value;
    }


    [Space(10)]

    public float minStartEnergy;
    public float maxStartEnergy;

    private void Awake()
    {
        brain = GetComponent<Brain>();
        rb = GetComponent<Rigidbody2D>();
        spriteRenderer = GetComponent<SpriteRenderer>();
        BecomeAlive();
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.collider.tag == "Creature")
        {
            Creature creature = collision.gameObject.GetComponent<Creature>();
            addEnergy(creature.GetAttacked(this));
            energy *= .5f;
            energy -= 10;
        } else
        {
            // Probably collided with a wall
            //Die();
        }
    }

    // Determines if the attacker would kill this creature
    public float GetAttacked(Creature attacker)
    {
        if (attacker.strength > strength + 3)
        {
            Die();
            return energy;
        }
        return 0;
    }

    public void Die()
    {
        dying = true;
    }

    // Set the values of the creature based on its parent and mutation
    public void BecomeAliveAndMutate(Creature parent)
    {
        transform.position = parent.gameObject.transform.position;
        gameObject.SetActive(true);
        dying = false;

        strength = parent.strength + Random.Range(-1,2);
        strength = Mathf.Max(strength, 0);

        birthCountdown = parent.birthCountdown + Random.Range(-50, 50);
        birthCountdown = Mathf.Max(birthCountdown,50);

        birthDelay = birthCountdown;

        energy = parent.energy/2;
        parent.energy /= 2;
        SetColor();

        brain.InheritFromParent(parent.brain);
    }

    // Method for first time creature creation
    public void BecomeAlive()
    {
        gameObject.SetActive(true);
        birthCountdown = Random.Range(0, 1000);
        birthDelay = birthCountdown;
        strength = Random.Range(0,10);
        energy = Random.Range(minStartEnergy, maxStartEnergy);

        SetColor();
    }

    public void SetColor()
    {
        float maxStrengthColorPercent = Mathf.Min((float)strength / maxDisplayedStrength, 1f);
        spriteRenderer.color = maxStrengthColorPercent * maxStrength + (1 - maxStrengthColorPercent) * minStrength;
    }

    public void GiveBirth()
    {
        birthCountdown = birthDelay;
        energy *= 0.7f;
        energy -= 100;
        if (energy > 0)
        {
            CreatureManager.single.CreateCreature(this);
        }
    }

    public void GiveBirth(Vector2 relativePos)
    {
        birthCountdown = birthDelay;
        energy *= 0.8f;
        energy -= 100;
        if (energy > 0)
        {
            CreatureManager.single.CreateCreature(this, relativePos);
        }
    }

    public void Think()
    {
        Dictionary<string, float> senses = new Dictionary<string, float>();
        senses.Add("energy",energy);
        brain.Think(senses);
        energy -= brain.GetEnergyUse();
    }

    public void DoMovement()
    {
        Swim();
        Turn();
    }

    private void Swim()
    {
        rb.AddForce(brain.GetSwimDirection());
    }

    public void Turn()
    {
        rb.rotation += brain.turnForce;
    }
}
